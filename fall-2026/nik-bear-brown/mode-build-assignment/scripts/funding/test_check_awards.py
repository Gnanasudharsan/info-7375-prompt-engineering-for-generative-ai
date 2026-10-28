#!/usr/bin/env python3
"""Tests for check-awards.py with canned database answers: no network."""
import datetime as dt, importlib.util, os, unittest, urllib.error, urllib.parse

spec = importlib.util.spec_from_file_location("ca", os.path.join(os.path.dirname(__file__), "check-awards.py"))
ca = importlib.util.module_from_spec(spec); spec.loader.exec_module(ca)
WS = dt.date(2027, 1, 1)


def nih_row(num, end, amount=100000, org="TESTU"):
    return {"project_num": num, "award_amount": amount, "project_start_date": "2025-01-01T00:00:00", "project_end_date": end + "T00:00:00",
            "organization": {"org_name": org}, "project_title": "A title", "fiscal_year": 2026, "agency_ic_admin": {"abbreviation": "NHGRI"}}


def fake(rows_by_org, nsf_rows=()):
    def f(url, body=None, timeout=60):
        if body is not None:
            org = body["criteria"]["org_names"][0]
            rows = rows_by_org.get(org, [])
            if "advanced_text_search" not in body["criteria"]:
                return {"meta": {"total": len(rows)}, "results": rows[:body.get("limit", 500)]}
            return {"meta": {"total": len(rows)}, "results": rows}
        return {"response": {"award": list(nsf_rows)}}
    return f


class Gates(unittest.TestCase):
    def test_activity_codes(self):
        self.assertEqual(ca.activity_code("5R01HG000001-07"), "R01")
        self.assertEqual(ca.activity_code("1K99AG000002-01A1"), "K99")
        self.assertEqual(ca.activity_code("7R01HG000003-02"), "R01")
        self.assertEqual(ca.activity_code("3UH3CA000004-04S1"), "UH3")

    def test_an_award_that_ends_before_the_window_plus_margin_fails_g1(self):
        self.assertFalse(ca.gates(dt.date(2027, 3, 1), "R01", WS, 6)["G1_active"])
        self.assertTrue(ca.gates(dt.date(2027, 7, 15), "R01", WS, 6)["G1_active"])
        self.assertFalse(ca.gates(None, "R01", WS, 6)["G1_active"])

    def test_fellowship_and_career_awards_are_trainee_only_and_unknown_codes_are_not_decided(self):
        self.assertEqual(ca.gates(dt.date(2030, 1, 1), "F31", WS, 6)["G2_type"], "trainee-only")
        self.assertEqual(ca.gates(dt.date(2030, 1, 1), "K99", WS, 6)["G2_type"], "trainee-only")
        self.assertEqual(ca.gates(dt.date(2030, 1, 1), "R01", WS, 6)["G2_type"], "research-project")
        self.assertEqual(ca.gates(dt.date(2030, 1, 1), "XYZ", WS, 6)["G2_type"], "unclassified")


class Run(unittest.TestCase):
    def test_a_wrong_organisation_name_is_reported_as_the_name_not_as_no_funding(self):
        awards, queries, status = ca.run(["TYPO UNIVERSITY"], ["single cell"], 2026, WS, 6, fetch=fake({"REAL U": [nih_row("5R01HG000001-01", "2030-01-01")]}), sources=("nih",))
        self.assertEqual(awards, [])
        self.assertFalse(status["TYPO UNIVERSITY"]["name_matched"])
        self.assertEqual([q["purpose"] for q in queries if q.get("purpose")], ["control (G3)"])     # no topic query was run

    def test_nih_amounts_are_labelled_annual_and_nsf_amounts_total_and_never_summed(self):
        nsf = [{"id": "1234567", "title": "T", "startDate": "01/01/2025", "expDate": "12/31/2030", "estimatedTotalAmt": "900000", "fundsObligatedAmt": "300000", "awardeeName": "REAL U", "fundProgramName": "CISE"}]
        awards, _, _ = ca.run(["REAL U"], ["single cell"], 2026, WS, 6, fetch=fake({"REAL U": [nih_row("5R01HG000001-01", "2030-01-01", 500000, "REAL U")]}, nsf))
        kinds = {a["source"]: a["amount_kind"] for a in awards}
        self.assertIn("annual", kinds["nih_reporter"]); self.assertIn("total", kinds["nsf_award_search"])
        s = ca.summarise(awards, ["REAL U"])["REAL U"]
        self.assertEqual(s["nih_annual_amount_of_passing_awards"], 500000)          # the NSF 900000 is not in it

    def test_trainee_awards_are_kept_in_the_output_but_do_not_count_as_passing(self):
        rows = [nih_row("5R01HG000001-01", "2030-01-01", org="REAL U"), nih_row("1K99AG000002-01", "2030-01-01", org="REAL U"), nih_row("5R01HG000003-01", "2026-12-01", org="REAL U")]
        awards, _, _ = ca.run(["REAL U"], ["x"], 2026, WS, 6, fetch=fake({"REAL U": rows}), sources=("nih",))
        s = ca.summarise(awards, ["REAL U"])["REAL U"]
        self.assertEqual((s["found"], s["pass_G1_and_G2"], s["trainee_only"], s["ended_before_window_plus_margin"]), (3, 1, 1, 1))

    def test_the_control_query_makes_exactly_one_request(self):
        calls = []
        base = fake({"REAL U": [nih_row("5R01HG00000%d-01" % i, "2030-01-01", org="REAL U") for i in range(5)]})
        def counting(url, body=None, timeout=60):
            calls.append(body["criteria"].get("advanced_text_search") if body else "nsf")
            return base(url, body, timeout)
        ca.run(["REAL U"], [], 2026, WS, 6, fetch=counting, sources=("nih",))
        self.assertEqual(len(calls), 1)          # a control query that paged through every award once looked like a hang

    def test_ids_can_be_redacted_for_tracked_outputs_and_the_stand_in_is_stable(self):
        a = {"award_id": "5R01HG000001-01", "activity_code": "R01", "org": "REAL U"}
        r1, r2 = ca.redact([a])[0], ca.redact([dict(a)])[0]
        self.assertNotIn("5R01HG000001", r1["award_id"]); self.assertEqual(r1["award_id"], r2["award_id"]); self.assertTrue(r1["award_id"].startswith("redacted-R01-"))

    def test_the_private_file_must_sit_under_a_private_directory(self):
        self.assertTrue(ca.private_path_ok("private/funding/x.json")); self.assertTrue(ca.private_path_ok("/a/b/private/x.json"))
        self.assertFalse(ca.private_path_ok("runs/x.json")); self.assertFalse(ca.private_path_ok("/a/privately/x.json"))

    def test_with_pi_without_a_private_file_is_refused(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(ca.main(["--orgs", "X", "--terms", "y", "--window-start", "2027-01-01", "--with-pi", "--out-json", d + "/a.json", "--out-md", d + "/a.md"]), 2)
            self.assertEqual(ca.main(["--orgs", "X", "--terms", "y", "--window-start", "2027-01-01", "--private-file", d + "/a.json", "--out-json", d + "/b.json", "--out-md", d + "/b.md"]), 2)

    def test_no_person_field_is_ever_requested_or_written_by_default(self):
        self.assertFalse([f for f in ca.NIH_FIELDS if "investigator" in f.lower() or f.lower().startswith("pi")])
        awards, _, _ = ca.run(["REAL U"], ["x"], 2026, WS, 6, fetch=fake({"REAL U": [{**nih_row("5R01HG000001-01", "2030-01-01", org="REAL U"), "principal_investigators": [{"full_name": "Someone"}]}]}), sources=("nih",))
        self.assertNotIn("Someone", str(awards))

    def test_nsf_results_are_paged_so_a_full_first_page_is_not_mistaken_for_all_of_them(self):
        pages = {1: [{"id": str(i)} for i in range(25)], 26: [{"id": str(i)} for i in range(25, 31)]}
        def f(url, body=None, timeout=60):
            off = int(urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["offset"][0])
            return {"response": {"award": pages.get(off, [])}}
        rows, truncated = ca.nsf_query("X", "y", WS, f)
        self.assertEqual((len(rows), truncated), (31, False))

    def test_investigators_go_to_the_private_sidecar_only(self):
        row = {**nih_row("5R01HG000001-01", "2030-01-01", org="REAL U"), "principal_investigators": [{"full_name": "Someone Else"}]}
        sidecar = {}
        awards, _, _ = ca.run(["REAL U"], ["x"], 2026, WS, 6, fetch=fake({"REAL U": [row]}), sources=("nih",), with_pi=True, sidecar=sidecar)
        self.assertEqual(sidecar["5R01HG000001-01"]["principal_investigators"], ["Someone Else"])
        self.assertNotIn("Someone Else", str(awards))

    def test_a_partial_name_that_matches_several_organisations_is_reported(self):
        rows = [nih_row("5R01HG000001-01", "2030-01-01", org="REAL U MEDICAL SCHOOL"), nih_row("5R01HG000002-01", "2030-01-01", org="REAL U SCHOOL OF PUBLIC HEALTH")]
        _, _, status = ca.run(["REAL U"], ["x"], 2026, WS, 6, fetch=fake({"REAL U": rows}), sources=("nih",))
        self.assertEqual(status["REAL U"]["returned_org_names"], ["REAL U MEDICAL SCHOOL", "REAL U SCHOOL OF PUBLIC HEALTH"])

    def test_nsf_awards_to_other_awardees_are_dropped_and_counted_not_attributed_to_the_institution(self):
        nsf = [{"id": "1", "title": "T", "expDate": "12/31/2030", "estimatedTotalAmt": "100", "awardeeName": "Real U."},
               {"id": "2", "title": "T", "expDate": "12/31/2030", "estimatedTotalAmt": "100", "awardeeName": "Some Other University"}]
        awards, queries, _ = ca.run(["REAL U"], ["x"], 2026, WS, 6, fetch=fake({"REAL U": []}, nsf), sources=("nsf",))
        self.assertEqual([a["award_id"] for a in awards], ["1"])
        q = [q for q in queries if q["source"] == "nsf_award_search"][0]
        self.assertEqual((q["fetched"], q["kept_exact_awardee_name"], q["dropped_other_awardees"]), (2, 1, 1))

    def test_nsf_stops_at_the_page_cap_and_says_the_result_is_truncated(self):
        def always_full(url, body=None, timeout=60):
            return {"response": {"award": [{"id": "1"}] * 25}}
        rows, truncated = ca.nsf_query("X", "y", WS, always_full)
        self.assertTrue(truncated); self.assertEqual(len(rows), 25 * ca.NSF_MAX_PAGES)

    def test_an_unreachable_database_stops_the_run_instead_of_reporting_zero(self):
        def down(url, body=None, timeout=60):
            raise urllib.error.URLError("unreachable")
        with self.assertRaises(urllib.error.URLError):
            ca.run(["REAL U"], ["x"], 2026, WS, 6, fetch=down, sources=("nih",))


if __name__ == "__main__":
    unittest.main()
