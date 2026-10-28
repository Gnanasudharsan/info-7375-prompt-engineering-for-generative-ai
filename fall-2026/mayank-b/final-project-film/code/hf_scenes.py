#!/usr/bin/env python3
"""hf_scenes.py — writes one HyperFrames project per body beat: hyperframes/<BID>/index.html.

Each composition lasts exactly the beat's narration (actual_duration_s) and every entrance is
keyed to a spoken word from mp3/words.json, so the picture lands when the voice names it.
Palette, type and layout rules: hyperframes/DESIGN.md. Real outputs shown on screen are copied
from slice/evidence/ (B05, B07, B09); nothing else claims to have run.
Render with the toolkit: python3 $TK/runtime/scripts/hyperframes_scenes.py <reel>.
"""
import json
import re
import shutil
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
HF = REEL / "hyperframes"
GSAP = Path.home() / "Desktop/Nate_Herk/herk-edit-kit/node_modules/gsap/dist/gsap.min.js"

sheet = json.loads((REEL / "beat_sheet.json").read_text())
words = json.loads((REEL / "mp3/words.json").read_text())
FPS = words["fps"]


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def cues(bid, spec):
    """spec: {name: word | (word, nth) | (word, nth, offset_s)} -> {name: seconds}"""
    ws = [(norm(w["text"]), w["startFrame"] / FPS) for w in words["beats"][bid]]
    out = {}
    for name, v in spec.items():
        word, nth, off = (v, 1, 0.0) if isinstance(v, str) else (tuple(v) + (0.0,))[:3]
        hits = [t for w, t in ws if w == norm(word)]
        if len(hits) < nth:
            raise SystemExit(f"{bid}: cue word '{word}' #{nth} not in narration")
        out[name] = round(max(0.15, hits[nth - 1] + off), 3)
    return out


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1920px;height:1080px;overflow:hidden;background:#FAF9F5;color:#3D3929;font-family:Inter,Arial,sans-serif}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:#FAF9F5}
.stage{position:absolute;left:120px;top:70px;width:1680px;height:790px;display:flex;flex-direction:column;gap:40px}
.stage>.h+*{margin-top:auto}.stage>*:last-child{margin-bottom:auto}
.chip{position:absolute;right:120px;top:66px;font:700 30px Inter,Arial,sans-serif;letter-spacing:1px;padding:10px 24px;border:3px solid #3D3929;border-radius:999px;background:#FFFFFF;color:#3D3929}
.chip.real{background:#3D3929;color:#FAF9F5}
.h{font:800 64px/1.1 Inter,Arial,sans-serif;letter-spacing:-1.5px;max-width:1260px}
.sub{font:500 36px/1.35 Inter,Arial,sans-serif;color:#6B6857}
.row{display:flex;gap:34px;align-items:stretch}
.col{display:flex;flex-direction:column;gap:22px}
.card{background:#FFFFFF;border:3px solid #E5E2D9;border-radius:22px;padding:32px 38px}
.card.focus{border-color:#D97757}
.lbl{font:700 30px Inter,Arial,sans-serif;color:#6B6857;letter-spacing:.5px}
.big{font:600 48px/1.3 Inter,Arial,sans-serif}
.body{font:500 38px/1.35 Inter,Arial,sans-serif}
.mark{background:#F6DCCF;border-bottom:6px solid #D97757;padding:0 10px;border-radius:8px}
.mono{font-family:'JetBrains Mono',Menlo,monospace}
.stamp{display:inline-block;font:800 40px Inter,Arial,sans-serif;color:#FFFFFF;padding:10px 30px;border-radius:12px;letter-spacing:2px}
.hold{background:#A3402A}.pass{background:#3E6B4C}
.term{background:#2B2A25;color:#F3F1EA;border-radius:20px;padding:32px 40px;font:500 33px/1.55 'JetBrains Mono',Menlo,monospace}
.term .ok{color:#9FD3A8}.term .bad{color:#E8A487}.term .dim{color:#B9B5A6}
.arrow{flex:0 0 auto;align-self:center;width:90px;height:8px;background:#3D3929;position:relative;border-radius:4px}
.arrow:after{content:"";position:absolute;right:-6px;top:-13px;border-left:26px solid #3D3929;border-top:17px solid transparent;border-bottom:17px solid transparent}
.tick{color:#3E6B4C;font-weight:800}.cross{color:#A3402A;font-weight:800}
"""

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>%%BID%%</title>
<script src="assets/gsap.min.js"></script>
<style>%%CSS%%
%%XCSS%%</style></head><body>
<div id="root" data-composition-id="%%BID%%" data-start="0" data-duration="%%DUR%%" data-width="1920" data-height="1080">
<div id="scene" class="clip" data-start="0" data-duration="%%DUR%%" data-track-index="1">
%%CHIP%%
<div class="stage">
%%BODY%%
</div></div></div>
<script>
const C=%%CUES%%;
const tl=gsap.timeline({paused:true});
const IN=(s,t,v)=>tl.from(s,Object.assign({opacity:0,y:28,duration:.55,ease:'power3.out'},v||{}),t);
%%JS%%
window.__timelines=window.__timelines||{};window.__timelines['%%BID%%']=tl;
</script></body></html>
"""

B = {}

# ── BWHO: who is doing it ────────────────────────────────────────────────────────────────
B["BWHO"] = dict(chip="", cues={"name": ("im", 1, -0.3), "school": "northeastern",
                                "claude": "claude", "me": "decide"},
    xcss=".nm{font:800 104px/1.05 Inter,Arial,sans-serif;letter-spacing:-3px}.split .card{flex:1}"
         ".split li{font:500 36px/1.5 Inter,Arial,sans-serif;list-style:none}.split li:before{content:'— ';color:#D97757}",
    body="""
<div class="lbl" id="who">WHO IS DOING IT</div>
<div class="nm" id="nm">Mayank Bhadrasen</div>
<div class="big" id="sch">M.S. Information Systems · Northeastern University</div>
<div class="row split" id="split">
  <div class="card focus" id="me"><div class="lbl">ME</div><ul><li>decide what to build</li><li>decide what counts as correct</li><li>review every change</li></ul></div>
  <div class="card" id="cl"><div class="lbl">CLAUDE CODE (ASSISTANT)</div><ul><li>writes code with me</li><li>drafts docs I edit</li><li>the log records who did what</li></ul></div>
</div>""",
    js="IN('#who',C.name-.2);IN('#nm',C.name,{y:40,duration:.7});IN('#sch',C.school-.4);"
       "IN('#cl',C.claude,{x:40,y:0});IN('#me',C.me-.3,{x:-40,y:0,ease:'back.out(1.4)'});")

# ── BKID: the idea, simply ───────────────────────────────────────────────────────────────
ROBOT = ('<svg width="170" height="190" viewBox="0 0 170 190"><line x1="85" y1="6" x2="85" y2="34" stroke="#3D3929" stroke-width="8"/>'
         '<circle cx="85" cy="10" r="10" fill="#D97757"/><rect x="14" y="34" width="142" height="112" rx="30" fill="#FFFFFF" stroke="#3D3929" stroke-width="8"/>'
         '<circle cx="58" cy="88" r="13" fill="#3D3929"/><circle cx="112" cy="88" r="13" fill="#3D3929"/>'
         '<rect x="56" y="114" width="58" height="10" rx="5" fill="#3D3929"/><rect x="40" y="152" width="90" height="34" rx="12" fill="#E5E2D9" stroke="#3D3929" stroke-width="6"/></svg>')
PERSON = ('<svg width="120" height="150" viewBox="0 0 120 150"><circle cx="60" cy="38" r="30" fill="#FFFFFF" stroke="#3D3929" stroke-width="8"/>'
          '<path d="M12 146 Q12 78 60 78 Q108 78 108 146 Z" fill="#F6DCCF" stroke="#3D3929" stroke-width="8"/></svg>')
BOOK = ('<svg width="200" height="130" viewBox="0 0 200 130"><path d="M100 18 Q60 0 10 10 V118 Q60 108 100 126 Z" fill="#FFFFFF" stroke="#3D3929" stroke-width="7"/>'
        '<path d="M100 18 Q140 0 190 10 V118 Q140 108 100 126 Z" fill="#FFFFFF" stroke="#3D3929" stroke-width="7"/>'
        '<line x1="28" y1="40" x2="84" y2="46" stroke="#E5E2D9" stroke-width="8"/><line x1="28" y1="64" x2="84" y2="70" stroke="#E5E2D9" stroke-width="8"/>'
        '<line x1="116" y1="46" x2="172" y2="40" stroke="#D97757" stroke-width="8"/><line x1="116" y1="70" x2="172" y2="64" stroke="#E5E2D9" stroke-width="8"/></svg>')
B["BKID"] = dict(chip="", cues={"robot": "robot", "sure": "sure", "wrong": "wrong", "checker": "checker",
                               "book": "rule", "agrees": "agrees", "not": "not", "person": "person"},
    xcss=".scene3{display:flex;gap:40px;align-items:center;margin-top:20px}.bub{position:relative;font:600 40px/1.3 Inter,Arial,sans-serif;max-width:470px}"
         ".bub:after{content:'';position:absolute;left:-26px;top:40px;border-right:30px solid #FFFFFF;border-top:18px solid transparent;border-bottom:18px solid transparent}"
         ".door{width:360px;height:450px;border:10px solid #3D3929;border-bottom:none;border-radius:150px 150px 0 0;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:12px;padding-bottom:20px;background:#FFFFFF}"
         ".outs{display:flex;flex-direction:column;gap:30px}.stamp,.lbl{white-space:nowrap}.out{display:flex;align-items:center;gap:20px;font:700 38px Inter,Arial,sans-serif}"
         ".x{position:absolute;right:24px;bottom:-34px;font:800 38px Inter,Arial,sans-serif}",
    body=f"""
<div class="h" id="hd">The idea, simply</div>
<div class="scene3">
  <div class="col" id="rb" style="align-items:center">{ROBOT}<div class="lbl">robot helper</div></div>
  <div class="card bub" id="bub">“Sure! You can claim that after your trip.”<span class="stamp hold x" id="xw">wrong</span></div>
  <div class="door" id="door"><div id="bk">{BOOK}</div><div class="lbl" style="text-align:center">checker with<br>the rule book</div></div>
  <div class="outs">
    <div class="out" id="o1"><span class="stamp pass">goes out</span><span class="body">the book agrees</span></div>
    <div class="out" id="o2">{PERSON}<span class="body">a person looks first</span></div>
  </div>
</div>""",
    js="IN('#hd',.2);IN('#rb',C.robot-.3,{scale:.7,y:0,ease:'back.out(1.6)'});IN('#bub',C.sure-.6,{x:-40,y:0});"
       "IN('#xw',C.wrong,{scale:2,opacity:0,y:0,ease:'back.out(2)'});IN('#door',C.checker-.2,{y:60});IN('#bk',C.book,{scale:.5,y:0,ease:'back.out(1.8)'});"
       "IN('#o1',C.agrees-.2,{x:-40,y:0});IN('#o2',C.person-.6,{x:-40,y:0,ease:'expo.out'});")

# ── B00: the real case ───────────────────────────────────────────────────────────────────
B["B00"] = dict(chip="real case", cues={"chat": "chatbot", "after": "after", "policy": "policy", "before": "before",
                                        "flip": "flipped", "trib": "tribunal"},
    xcss=".vs{display:flex;gap:30px;align-items:center}.vs .card{flex:1;min-height:300px;display:flex;flex-direction:column;gap:20px}"
         ".neq{font:800 120px Inter,Arial,sans-serif;color:#A3402A}.case{font:600 34px/1.4 Inter,Arial,sans-serif;border-left:10px solid #D97757;padding-left:26px}",
    body="""
<div class="h" id="hd">This already happened</div>
<div class="vs">
  <div class="card" id="bot"><div class="lbl">AIR CANADA'S CHATBOT (PARAPHRASED)</div><div class="big">You can claim a bereavement fare <span class="mark" id="m1">after</span> your trip.</div></div>
  <div class="neq" id="neq">≠</div>
  <div class="card" id="pol"><div class="lbl">THE AIRLINE'S POLICY (PARAPHRASED)</div><div class="big">The request must come <span class="mark" id="m2">before</span> travel.</div></div>
</div>
<div class="case" id="case">Moffatt v. Air Canada · BC Civil Resolution Tribunal · February 2024<br><span class="sub">The airline was held responsible for what its chatbot said.</span></div>""",
    js="IN('#hd',.2);IN('#bot',C.chat-.2,{x:-50,y:0});IN('#m1',C.after,{scale:1.6,opacity:0,y:0,ease:'back.out(2)'});"
       "IN('#pol',C.policy-.1,{x:50,y:0});IN('#m2',C.before,{scale:1.6,opacity:0,y:0,ease:'back.out(2)'});"
       "IN('#neq',C.flip-.2,{scale:.2,y:0,ease:'elastic.out(1,.5)',duration:.9});IN('#case',C.trib-.2);")

# ── B01: why it matters at scale ─────────────────────────────────────────────────────────
mini = "".join(f'<div class="card mini" id="m{i}">claim it <span class="mark">after</span> your trip</div>' for i in range(12))
B["B01"] = dict(chip="", cues={"same": "same", "every": "everyone", "prom": "promise", "net": "net", "later": "later"},
    xcss=".grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.mini{padding:18px 22px;font:600 31px Inter,Arial,sans-serif}"
         ".tline{display:flex;align-items:center;gap:22px;font:600 34px Inter,Arial,sans-serif}.tline .card{padding:18px 26px}",
    body=f"""
<div class="h" id="hd">One wrong rule, repeated to everyone</div>
<div class="grid" id="grid">{mini}</div>
<div class="tline" id="tl1"><div class="card">answer sent</div><div class="arrow"></div><div class="card">customers told</div><div class="arrow"></div>
<div class="card focus" id="late">transcripts reviewed later</div></div>""",
    js="IN('#hd',.2);IN('#m0',C.same-.3,{scale:.6,y:0,ease:'back.out(1.7)'});"
       "IN('.mini:not(#m0)',C.every,{scale:.6,y:0,stagger:.12,ease:'power2.out'});IN('#tl1',C.net-.3,{x:-40,y:0});"
       "IN('#late',C.later-.2,{scale:1.3,y:0,ease:'back.out(2)'});")

# ── B02: what I'm building ───────────────────────────────────────────────────────────────
B["B02"] = dict(chip="proposed design", cues={"sc": "source", "between": "between", "checks": "checks",
                                              "holds": "holds", "before": "before"},
    xcss=".flow{display:flex;align-items:center;gap:26px;margin-top:20px}.flow .card{font:700 40px Inter,Arial,sans-serif;text-align:center}"
         ".sc{border-width:6px!important;border-color:#3D3929!important;background:#F6DCCF!important;padding:36px 46px!important;font-size:48px!important}"
         ".notes{display:flex;gap:30px}.notes .card{flex:1}",
    body="""
<div class="h" id="hd">What I'm building: Source Check</div>
<div class="flow"><div class="card" id="bot">support bot</div><div class="arrow" id="a1"></div>
<div class="card sc" id="sc">Source Check</div><div class="arrow" id="a2"></div><div class="card" id="cu">customer</div></div>
<div class="notes">
  <div class="card" id="n1"><div class="lbl">CHECKS</div><div class="body">each policy answer against the current, dated policy</div></div>
  <div class="card" id="n2"><div class="lbl">HOLDS</div><div class="body">the answer for a person when the policy doesn't back it up</div></div>
  <div class="card focus" id="n3"><div class="lbl">WHEN</div><div class="body"><span class="mark">before</span> the customer sees it, not in a review afterwards</div></div>
</div>""",
    js="IN('#hd',.2);IN('#bot',.4,{x:-30,y:0});IN('#cu',.6,{x:30,y:0});IN('#a1,#a2',.8,{scaleX:0,y:0,transformOrigin:'left'});"
       "IN('#sc',C.between-.2,{y:-80,scale:.8,ease:'back.out(1.6)'});IN('#n1',C.checks-.1);IN('#n2',C.holds-.1);IN('#n3',C.before-.3,{ease:'expo.out'});")

# ── B03: architecture ────────────────────────────────────────────────────────────────────
steps = [("1", "n8n webhook", "the bot's draft answer arrives", "n8n"), ("2", "Claude", "splits it into claims", "claude"),
         ("3", "Python checker", "each claim vs the policy store", "python"), ("4", "pass or hold", "hold goes to Slack for a support lead", "passes"),
         ("5", "log", "decision + policy version", "logged")]
cells = '<div class="arrow"></div>'.join(
    f'<div class="card st" id="s{n}"><div class="num">{n}</div><div class="stt">{t}</div><div class="std">{d}</div></div>' for n, t, d, _ in steps)
B["B03"] = dict(chip="proposed design", cues={f"s{n}": w for n, _, _, w in steps},
    xcss=".arch{display:flex;align-items:stretch;gap:14px;margin-top:40px}.st{flex:1;display:flex;flex-direction:column;gap:14px;padding:28px 24px}"
         ".num{font:800 34px Inter,Arial,sans-serif;color:#FFFFFF;background:#3D3929;width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center}"
         ".stt{font:800 38px/1.15 Inter,Arial,sans-serif}.std{font:500 31px/1.35 Inter,Arial,sans-serif;color:#6B6857}.arch .arrow{width:40px}",
    body=f"""
<div class="h" id="hd">How it works, in five steps</div>
<div class="arch">{cells}</div>
<div class="sub" id="ft">One n8n workflow runs all five. It sits in front of any bot, so it doesn't replace one.</div>""",
    js="IN('#hd',.2);" + "".join(f"IN('#s{n}',C.s{n}-.25,{{y:50,ease:'back.out(1.5)'}});"
                                 f"tl.to('#s{n}',{{borderColor:'#D97757',duration:.3}},C.s{n});" for n, *_ in steps)
       + "IN('.arch .arrow',C.s1+.4,{scaleX:0,y:0,transformOrigin:'left',stagger:.6});IN('#ft',C.s5+.6);")

# ── B04: the prompt contract ─────────────────────────────────────────────────────────────
fields = [("topic", '"bereavement fare"', "topic"), ("relation", '"after"', "condition"), ("amount", "0", "amount"),
          ("unit", '"days"', "unit"), ("anchor", '"travel"', "measured")]
jl = "".join(f'<div id="f{i}">&nbsp;&nbsp;<span class="dim">"{k}"</span>: {"<span class=bad>" + v + "</span>" if k == "relation" else v}{"," if i < 4 else ""}</div>'
             for i, (k, v, _) in enumerate(fields))
B["B04"] = dict(chip="proposed design", cues={"json": "json", **{f"f{i}": w for i, (_, _, w) in enumerate(fields)},
                                              "val": "validates", "miss": "missing"},
    xcss=".two{display:flex;gap:40px;align-items:flex-start}.two>.card{flex:0 0 560px}.two .term{flex:1}",
    body=f"""
<div class="h" id="hd">Step 1 · the prompt contract</div>
<div class="two">
  <div class="card" id="ans"><div class="lbl">THE BOT'S ANSWER</div><div class="big">You can claim the bereavement fare <span class="mark">after</span> your trip.</div></div>
  <div class="term" id="js"><div class="dim">// Claude must return exactly these five fields</div><div>{{</div>{jl}<div>}}</div></div>
</div>
<div class="row" id="vrow"><span class="stamp pass" id="v1">valid: 5 of 5 fields</span><span class="body" id="v2">a field missing or extra → <span class="stamp hold">HOLD</span></span></div>""",
    js="IN('#hd',.2);IN('#ans',.5,{x:-40,y:0});IN('#js',C.json-.2,{x:40,y:0});"
       + "".join(f"IN('#f{i}',C.f{i}-.1,{{x:-20,y:0,duration:.4}});" for i in range(5))
       + "IN('#v1',C.val-.1,{scale:.6,y:0,ease:'back.out(2)'});IN('#v2',C.miss-.3);")

# ── B05: the check (real checker output) ────────────────────────────────────────────────
B["B05"] = dict(chip="real output", cues={"cur": "current", "field": "field", "after": "after", "before": "before",
                                          "mis": "mismatch", "reason": "reason", "ext": "extracts", "dec": "decides"},
    xcss="table{border-collapse:separate;border-spacing:0;width:100%;font:500 34px Inter,Arial,sans-serif;background:#FFFFFF;border:3px solid #E5E2D9;border-radius:22px;overflow:hidden}"
         "th{font:700 30px Inter,Arial,sans-serif;color:#6B6857;text-align:left;padding:16px 28px;border-bottom:3px solid #E5E2D9}"
         "td{padding:12px 28px;border-bottom:2px solid #F0EEE6}.bad-row td{background:#FBEDE6}.res{display:flex;gap:26px;align-items:center}"
         ".who{display:flex;gap:30px;font:700 34px Inter,Arial,sans-serif}",
    body="""
<div class="h" id="hd">Step 2 · plain code checks each field</div>
<table id="tb"><tr><th>field</th><th>claim (from the answer)</th><th>policy BRV-2026-03 (current)</th><th></th></tr>
<tr id="r0"><td>topic</td><td>bereavement fare</td><td>bereavement fare</td><td class="tick">✓</td></tr>
<tr id="r1" class="bad-row"><td>relation</td><td><span class="mark" id="ca">after</span> travel</td><td><span class="mark" id="cb">before</span> travel</td><td class="cross" id="cx">✗</td></tr>
<tr id="r2"><td>amount · unit</td><td>0 days</td><td>0 days</td><td class="tick">✓</td></tr></table>
<div class="res" id="res"><span class="stamp hold" id="st">HOLD</span><span class="body mono" id="rs">answer says 'after travel', policy says 'before travel'</span></div>
<div class="who" id="who"><span>Claude: extracts</span><span>·</span><span>Code: decides</span></div>""",
    js="IN('#hd',.2);IN('#tb',C.cur-.2);IN('#r0',C.field-.1,{x:-30,y:0});IN('#r2',C.field+.3,{x:-30,y:0});IN('#r1',C.after-.6,{x:-30,y:0});"
       "IN('#ca',C.after,{scale:1.5,opacity:0,y:0,ease:'back.out(2)'});IN('#cb',C.before,{scale:1.5,opacity:0,y:0,ease:'back.out(2)'});"
       "IN('#cx',C.mis-.2,{scale:2.5,y:0,ease:'back.out(2.5)'});IN('#st',C.mis+.3,{scale:2,y:0,ease:'back.out(2)'});IN('#rs',C.reason-.2,{x:-30,y:0});"
       "IN('#who',C.ext-.2,{ease:'expo.out'});")

# ── B06: pass or hold, the human gate ───────────────────────────────────────────────────
B["B06"] = dict(chip="proposed design", cues={"match": "matches", "log": "log", "src": "source", "old": "outdated",
                                              "con": "contradicts", "slack": "slack", "app": "approves"},
    xcss=".lane{display:flex;align-items:center;gap:26px}.lane .card{font:600 34px Inter,Arial,sans-serif}"
         ".slack{flex:1;display:flex;flex-direction:column;gap:14px;border-left:12px solid #A3402A!important}"
         ".btns{display:flex;gap:16px}.btn{font:700 30px Inter,Arial,sans-serif;padding:10px 24px;border:3px solid #3D3929;border-radius:10px}"
         ".why{display:flex;flex-direction:column;gap:10px;font:600 32px Inter,Arial,sans-serif}",
    body="""
<div class="h" id="hd">Pass, or hold for a person</div>
<div class="lane" id="pl"><span class="stamp pass">PASS</span><div class="arrow"></div><div class="card">sent to the customer</div>
<div class="card mono" id="lg" style="font-size:30px">log · PASS · policy RFD-2026-01</div></div>
<div class="lane" id="hl"><span class="stamp hold">HOLD</span>
  <div class="why"><span id="w1">no source</span><span id="w2">outdated version</span><span id="w3">contradicts the policy</span></div>
  <div class="arrow"></div>
  <div class="card slack" id="sl"><div class="lbl">SLACK · #support-holds (MOCK-UP)</div>
    <div class="body">Source Check held an answer: <span class="mono">answer says 'after travel', policy says 'before travel'</span></div>
    <div class="btns" id="bt"><span class="btn">Approve</span><span class="btn">Edit</span><span class="btn">Reject</span></div></div>
</div>""",
    js="IN('#hd',.2);IN('#pl',C.match-.3,{x:-40,y:0});IN('#lg',C.log-.1,{scale:.8,y:0,ease:'back.out(1.6)'});"
       "IN('#hl',C.src-.6,{x:-40,y:0});IN('#w1',C.src-.1,{x:-20,y:0});IN('#w2',C.old-.1,{x:-20,y:0});IN('#w3',C.con-.1,{x:-20,y:0});"
       "IN('#sl',C.slack-.3,{x:50,y:0,ease:'expo.out'});IN('#bt .btn',C.app-.2,{y:20,stagger:.35,ease:'back.out(2)'});")

# ── B07: what runs today (real pytest + mutation output, 2026-10-22) ─────────────────────
B["B07"] = dict(chip="real output", cues={"runs": "runs", "air": "air", "within": "within", "match": "matching",
                                          "all": "all", "broken": "broken", "fail": "fail", "hand": "hand"},
    xcss=".terms{display:flex;gap:30px}.terms .term{flex:1;font-size:30px}.foot{font:600 32px Inter,Arial,sans-serif;color:#6B6857}",
    body="""
<div class="h" id="hd">This part already runs</div>
<div class="terms">
<div class="term" id="t1"><div class="dim">$ python3 -m pytest -v</div>
<div id="l1">test_air_canada_shape_holds <span class="ok">PASSED</span></div>
<div id="l2">test_within_90_days_vs_90_days_after_holds <span class="ok">PASSED</span></div>
<div id="l3">test_matching_answer_passes_and_logs_version <span class="ok">PASSED</span></div>
<div id="l4" class="ok">21 passed in 0.02s</div></div>
<div class="term" id="t2" style="flex:0 0 640px"><div class="dim"># the check broken on purpose</div>
<div id="l5"><span class="dim">ignore before/after:</span> <span class="bad">6 failed</span></div>
<div id="l6"><span class="dim">ignore dates:</span> <span class="bad">6 failed</span></div>
<div id="l7"><span class="dim">allow extra fields:</span> <span class="bad">2 failed</span></div></div>
</div>
<div class="foot" id="ft">Run 2026-10-25 on synthetic data · claims written by hand · Claude extraction not built yet</div>""",
    js="IN('#hd',.2);IN('#t1',C.runs-.3,{x:-40,y:0});IN('#l1',C.air-.1,{x:-20,y:0,duration:.35});IN('#l2',C.within-.1,{x:-20,y:0,duration:.35});"
       "IN('#l3',C.match-.1,{x:-20,y:0,duration:.35});IN('#l4',C.all-.1,{scale:1.2,y:0,ease:'back.out(2)'});"
       "IN('#t2',C.broken-.3,{x:40,y:0});IN('#l5,#l6,#l7',C.fail-.3,{x:-20,y:0,stagger:.25,ease:'back.out(2)'});IN('#ft',C.hand-.4);")

# ── B08: alternatives ────────────────────────────────────────────────────────────────────
B["B08"] = dict(chip="", cues={"fin": "intercom", "sim": "simulations", "zen": "zendesks", "esc": "escalate", "man": "manual", "find": "find"},
    xcss=".alts{display:flex;gap:28px}.alts .card{flex:1;display:flex;flex-direction:column;gap:12px}.alts .big{font-size:40px;font-weight:800}.alts .body{font-size:34px}"
         ".gap{border:5px dashed #D97757;border-radius:22px;padding:24px 34px;font:600 36px/1.35 Inter,Arial,sans-serif;background:#FFFFFF}",
    body="""
<div class="h" id="hd">What already exists</div>
<div class="alts">
  <div class="card" id="a1"><div class="big">Intercom Fin</div><div class="body">AI agent trained on your policies and procedures</div><div class="body" id="a1b">tests changes in simulations before launch; hands hard cases to people</div><div class="lbl">fin.ai, read 2026-10-25</div></div>
  <div class="card" id="a2"><div class="big">Zendesk AI agents</div><div class="body">answers from the help-center articles you connect</div><div class="body" id="a2b">escalates to a human when it can't answer</div><div class="lbl">Zendesk help center docs, read 2026-10-25</div></div>
  <div class="card" id="a3"><div class="big">Manual review</div><div class="body">a lead reads transcripts <span class="mark">after</span> answers are sent</div><div class="lbl">common practice</div></div>
</div>
<div class="gap" id="gp">Not found on their public pages: a check of each answer, <span class="mark">at send time</span>, against the current dated policy.</div>""",
    js="IN('#hd',.2);IN('#a1',C.fin-.2,{y:50});IN('#a1b',C.sim-.3);IN('#a2',C.zen-.2,{y:50});IN('#a2b',C.esc-.3);IN('#a3',C.man-.2,{y:50});"
       "IN('#gp',C.find-.3,{scale:.9,y:0,ease:'back.out(1.5)'});")

# ── B09: who opens it (real demo output) ────────────────────────────────────────────────
B["B09"] = dict(chip="real output", cues={"lead": "lead", "hire": "hiring", "cmd": "command", "held": "held", "works": "works"},
    xcss=".pp{display:flex;gap:26px}.pp .card{font:700 36px Inter,Arial,sans-serif}",
    body="""
<div class="h" id="hd">Who opens it, and their first minute</div>
<div class="pp"><div class="card" id="p1">a support lead</div><div class="card" id="p2">a hiring manager</div></div>
<div class="term" id="tm"><div>$ python3 -m source_check.demo</div>
<div id="d1"><span class="dim">answer :</span> You can claim the bereavement fare after your trip, within 90 days.</div>
<div id="d2"><span class="dim">verdict:</span> <span class="bad">HOLD</span></div>
<div id="d3"><span class="dim">reason :</span> answer says 'after travel', policy says 'before travel'</div>
<div id="d4"><span class="dim">policy :</span> BRV-2026-03: Bereavement fares must be requested before travel.</div></div>
<div class="sub" id="ft">Real output, 2026-10-22 · the airline and its policies are fictional</div>""",
    js="IN('#hd',.2);IN('#p1',C.lead-.3,{x:-30,y:0});IN('#p2',C.hire-.2,{x:-30,y:0});IN('#tm',C.cmd-.3);"
       "IN('#d1',C.cmd+.5,{x:-20,y:0,duration:.35});IN('#d2',C.held-.1,{scale:1.3,y:0,ease:'back.out(2)'});"
       "IN('#d3',C.held+.6,{x:-20,y:0,duration:.35});IN('#d4',C.held+1.4,{x:-20,y:0,duration:.35});IN('#ft',C.works-.2);")

# ── B10: what it will prove, and how it will be measured ────────────────────────────────
sk = [("prompt contracts", "prompt"), ("source grounding", "source"), ("deterministic checks", "deterministic"),
      ("approval gates", "approval"), ("evaluation", "evaluation")]
tiles = "".join(f'<div class="card tile" id="k{i}">{t}</div>' for i, (t, _) in enumerate(sk))
B["B10"] = dict(chip="proposed design", cues={**{f"k{i}": w for i, (_, w) in enumerate(sk)},
                                              "slip": "slip", "good": "good", "num": "numbers"},
    xcss=".tiles{display:flex;gap:18px}.tile{flex:1;font:700 38px/1.2 Inter,Arial,sans-serif;text-align:center;padding:26px 18px}"
         ".sets{display:flex;gap:22px}.sets .card{flex:1;font:600 38px Inter,Arial,sans-serif;text-align:center}"
         ".meters{display:flex;gap:28px}.meter{flex:1;display:flex;flex-direction:column;gap:12px}"
         ".bar{height:30px;border:3px dashed #6B6857;border-radius:15px}.mlab{font:600 38px Inter,Arial,sans-serif}",
    body=f"""
<div class="h" id="hd">What it will prove, and how it will be measured</div>
<div class="tiles">{tiles}</div>
<div class="sets" id="sets"><div class="card">correct answers</div><div class="card">outdated answers</div><div class="card">invented answers</div></div>
<div class="meters"><div class="meter" id="m1"><div class="mlab">wrong answers that slip through: <span class="mark">not measured yet</span></div><div class="bar"></div></div>
<div class="meter" id="m2"><div class="mlab">good answers that get held: <span class="mark">not measured yet</span></div><div class="bar"></div></div></div>""",
    js="IN('#hd',.2);" + "".join(f"IN('#k{i}',C.k{i}-.15,{{y:40,ease:'back.out(1.6)'}});" for i in range(5))
       + "IN('#sets',C.k4+.6);IN('#m1',C.slip-.4,{x:-30,y:0});IN('#m2',C.good-.3,{x:-30,y:0});"
         "tl.to('.meter .mark',{backgroundColor:'#F6DCCF',scale:1.08,duration:.3,yoyo:true,repeat:1},C.num);")

# ── B11: scope and the biggest risk ─────────────────────────────────────────────────────
B["B11"] = dict(chip="proposed design", cues={"scope": "scope", "out": "wont", "risk": "risk", "drop": "dropping",
                                              "def": "default", "flips": "flips"},
    xcss=".sr{display:flex;gap:34px}.sr>.card{flex:1;display:flex;flex-direction:column;gap:14px}.sr li{font:500 34px/1.45 Inter,Arial,sans-serif;list-style:none}"
         ".claim{font:600 40px 'JetBrains Mono',Menlo,monospace;display:flex;gap:16px;align-items:center}"
         ".gone{display:inline-block}.flips{font:500 31px/1.5 'JetBrains Mono',Menlo,monospace;color:#3D3929}",
    body="""
<div class="h" id="hd">Scope, and the biggest risk</div>
<div class="sr">
  <div class="card" id="sc"><div class="lbl">IN</div><ul><li>refunds, fees, eligibility</li><li>one fictional airline</li><li>synthetic data, English</li></ul>
  <div class="lbl" id="ol">OUT</div><ul id="ou"><li>writing answers</li><li>replacing the bot</li></ul></div>
  <div class="card focus" id="rk"><div class="lbl">RISK · CLAUDE DROPS A CONDITION WORD</div>
    <div class="claim"><span>"relation":</span><span class="mark gone" id="gw">"before"</span></div>
    <div class="row" id="df" style="align-items:center"><span class="body">unsure → default</span><span class="stamp hold">HOLD</span></div>
    <div class="flips" id="fl"><div>test set: condition flips</div><div>before ↔ after</div><div>within 90 days ↔ 90 days after</div><div>of booking ↔ before departure</div></div></div>
</div>""",
    js="IN('#hd',.2);IN('#sc',C.scope-.2,{x:-40,y:0});IN('#ol,#ou',C.out-.2);IN('#rk',C.risk-.3,{x:40,y:0});"
       "tl.to('#gw',{y:-50,opacity:0,duration:.7,ease:'power2.in'},C.drop+.2);IN('#df',C['def']-.3,{ease:'back.out(1.6)'});IN('#fl',C.flips-.6);")

# ── B12: why me, exists vs will exist ───────────────────────────────────────────────────
B["B12"] = dict(chip="", cues={"new": "new", "next": "next"},
    xcss=".ew{display:flex;gap:34px}.ew .card{flex:1;display:flex;flex-direction:column;gap:12px}.ew li{font:500 34px/1.5 Inter,Arial,sans-serif;list-style:none}"
         ".ew .e li:before{content:'✓ ';color:#3E6B4C;font-weight:800}.ew .w li:before{content:'○ ';color:#6B6857}",
    body="""
<div class="h" id="hd">What's new for me, and what comes next</div>
<div class="ew">
  <div class="card e" id="ex"><div class="lbl">EXISTS TODAY</div><ul><li id="e1">n8n + Claude workflows in my public repos</li>
  <li>this brief, its research, this film</li><li>the checker + 21 tests (slice/)</li></ul></div>
  <div class="card w" id="wl"><div class="lbl">WILL EXIST</div><ul><li>Claude extraction under the contract</li><li>the n8n workflow</li>
  <li>the Slack hold queue</li><li>a labelled test set, misses measured</li></ul></div>
</div>
<div class="sub" id="nw">New for me: building an evaluation set and measuring the misses.</div>""",
    js="IN('#hd',.2);IN('#ex',.5,{x:-40,y:0});IN('#nw',C['new']-.3);IN('#wl',C.next-.2,{x:40,y:0,ease:'expo.out'});")


def chip_html(chip):
    if not chip:
        return ""
    cls = "chip real" if chip.startswith("real") else "chip"
    return f'<div class="{cls}" id="chip">{chip}</div>'


def main():
    beats = {b["beat_id"]: b for b in sheet["beats"]}
    for bid, spec in B.items():
        beat = beats[bid]
        dur = beat["actual_duration_s"]
        c = cues(bid, spec["cues"])
        out = HF / bid
        (out / "assets").mkdir(parents=True, exist_ok=True)
        shutil.copy(GSAP, out / "assets/gsap.min.js")
        shutil.copy(HF / "DESIGN.md", out / "DESIGN.md")
        js = spec["js"] + ("IN('#chip',.1,{y:-20});" if spec["chip"] else "")
        html = (PAGE.replace("%%CSS%%", CSS).replace("%%XCSS%%", spec.get("xcss", ""))
                .replace("%%BID%%", bid).replace("%%DUR%%", f"{dur:.3f}").replace("%%CHIP%%", chip_html(spec["chip"]))
                .replace("%%BODY%%", spec["body"]).replace("%%CUES%%", json.dumps(c)).replace("%%JS%%", js))
        (out / "index.html").write_text(html)
        (out / "meta.json").write_text(json.dumps({"id": bid, "name": bid, "width": 1920, "height": 1080, "fps": FPS}) + "\n")
        late = {k: v for k, v in c.items() if v > dur - 0.4}
        print(f"{bid}: {dur:.2f}s, {len(c)} cues" + (f"  WARNING late cues {late}" if late else ""))


if __name__ == "__main__":
    main()
