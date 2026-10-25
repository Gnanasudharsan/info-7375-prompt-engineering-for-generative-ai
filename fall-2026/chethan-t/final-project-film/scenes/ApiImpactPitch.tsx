/**
 * ApiImpactPitch — reel-local compositions for "API Impact — The Pitch"
 * (Chethan Gowda, INFO 7375 final-project pitch film, 2026-10-13).
 *
 * Claude fidelity palette on the cream stage; ONE terracotta moment per beat.
 * Every scene is a pure function of frame / durationSeconds (the audio clock):
 * reveals are placed at fractions of the beat, matching the beat sheet's
 * shot.show events.
 *
 * Honesty: each scene carries the label its beat sheet declares (REAL /
 * CONSTRUCTED / PLANNED). Real code and the grep counts come from
 * gothinkster/angular-realworld-example-app @ dd99ed2 (MIT), read 2026-10-13.
 * Nothing here is output of the (not yet built) tool.
 *
 * No channel persona: the corner bug is the author's name, not @NikBearBrown.
 */
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {z} from 'zod';
import {CLAUDE, CLAUDE_FONT} from './tokens/claude';
import {SAFE} from './tokens/layout';

const SERIF = CLAUDE_FONT.serif;
const SANS = CLAUDE_FONT.ui;
const MONO = CLAUDE_FONT.mono;
// Terracotta on cream is ~2.7:1 — never body text. Use it for fills, rules, outlines.
const ACCENT_TINT = 'rgba(217,119,87,0.12)';

export const aipSchema = z.object({
  durationSeconds: z.number().default(15),
  sparkLine: z.string().default(''),
});
export type AipProps = z.infer<typeof aipSchema>;

export const aipOutroSchema = z.object({
  durationSeconds: z.number().default(5),
  title: z.string().default('API Impact.'),
  name: z.string().default('Chethan Gowda'),
  subline: z.string().default(''),
});
export type AipOutroProps = z.infer<typeof aipOutroSchema>;

const clamp01 = (v: number) => Math.min(1, Math.max(0, v));

/** Reveal progress (0→1) for an element that appears at fraction `at` of the beat. */
const useReveal = (durationSeconds: number) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const total = Math.max(1, durationSeconds * fps);
  return (at: number) =>
    clamp01(spring({frame: frame - at * total, fps, config: {damping: 26, stiffness: 120, mass: 0.9}}));
};

const rise = (p: number, px = 18): React.CSSProperties => ({
  opacity: p,
  transform: `translateY(${(1 - p) * px}px)`,
});

// ── shared chrome ────────────────────────────────────────────────────────────

const Label: React.FC<{text: string; kind: 'real' | 'constructed' | 'planned'}> = ({text, kind}) => (
  <div style={{
    position: 'absolute', top: SAFE.y + 6, right: 1920 - SAFE.r + 6,
    fontFamily: SANS, fontSize: 22, fontWeight: 700, letterSpacing: 2.5,
    textTransform: 'uppercase', color: CLAUDE.INK,
    background: kind === 'constructed' ? ACCENT_TINT : CLAUDE.PILL,
    border: `2px ${kind === 'planned' ? 'dashed' : 'solid'} ${kind === 'real' ? CLAUDE.INK_SOFT : CLAUDE.SPARK}`,
    borderRadius: 999, padding: '8px 20px', maxWidth: 1100,
    whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
  }}>{text}</div>
);

const Title: React.FC<{text: string; p: number}> = ({text, p}) => (
  <div style={{
    position: 'absolute', top: SAFE.y + 4, left: SAFE.x + 6, maxWidth: 1000,
    fontFamily: SERIF, fontSize: 64, fontWeight: 600, color: CLAUDE.INK, lineHeight: 1.1,
    ...rise(p, 12),
  }}>{text}</div>
);

const Spark: React.FC<{size?: number}> = ({size = 34}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" style={{flexShrink: 0}}>
    {[0, 30, 60, 90, 120, 150].map((r) => (
      <rect key={r} x={11} y={1} width={2} height={22} rx={1} fill={CLAUDE.SPARK}
        transform={`rotate(${r} 12 12)`} />
    ))}
  </svg>
);

/** Spark line (≤4 words) bottom-left + author wordmark bottom-right. */
const Footer: React.FC<{sparkLine: string; p: number}> = ({sparkLine, p}) => (
  <>
    {sparkLine ? (
      <div style={{
        position: 'absolute', left: SAFE.x + 6, bottom: 1080 - SAFE.b + 8,
        display: 'flex', alignItems: 'center', gap: 14, ...rise(p, 8),
      }}>
        <Spark />
        <span style={{fontFamily: SERIF, fontSize: 40, fontStyle: 'italic', color: CLAUDE.INK}}>{sparkLine}</span>
      </div>
    ) : null}
    <div style={{
      position: 'absolute', right: 1920 - SAFE.r + 6, bottom: 1080 - SAFE.b + 12,
      fontFamily: SERIF, fontSize: 26, color: CLAUDE.INK_SOFT, opacity: 0.85,
    }}>Chethan Gowda</div>
  </>
);

const Card: React.FC<{style?: React.CSSProperties; accent?: boolean; children: React.ReactNode}> = ({style, accent, children}) => (
  <div style={{
    background: CLAUDE.CARD, border: `2px solid ${accent ? CLAUDE.SPARK : CLAUDE.BORDER}`,
    borderRadius: 18, boxShadow: '0 6px 22px rgba(61,57,41,0.08)', padding: '24px 30px', ...style,
  }}>{children}</div>
);

const Eyebrow: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
  <div style={{fontFamily: SANS, fontSize: 22, fontWeight: 700, letterSpacing: 3, textTransform: 'uppercase',
    color: CLAUDE.INK_SOFT, ...style}}>{children}</div>
);

const Check: React.FC<{ok: boolean; size?: number}> = ({ok, size = 40}) => (
  <svg width={size} height={size} viewBox="0 0 40 40" style={{flexShrink: 0}}>
    {ok ? (
      <path d="M8 21 L17 30 L33 11" stroke={CLAUDE.INK} strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    ) : (
      <path d="M10 10 L30 30 M30 10 L10 30" stroke={CLAUDE.SPARK} strokeWidth={5} strokeLinecap="round" />
    )}
  </svg>
);

const Stage: React.FC<{children: React.ReactNode}> = ({children}) => (
  <AbsoluteFill style={{background: CLAUDE.PAGE}}>{children}</AbsoluteFill>
);

// ── B00 · open: who, what, for whom (replaces the Claude composer cold open) ─

export const AipOpen: React.FC<AipProps> = ({durationSeconds}) => {
  const r = useReveal(durationSeconds);
  const facts = [
    {k: 'By', v: 'Chethan Gowda', at: 0.2},
    {k: 'Target role', v: 'AI Software Development Engineer', at: 0.35},
    {k: 'Status', v: 'Planned — design and evaluation plan', at: 0.5},
  ];
  return (
    <Stage>
      <div style={{position: 'absolute', top: SAFE.y + 10, left: SAFE.x + 6, ...rise(r(0))}}>
        <Eyebrow>Portfolio project · 2026</Eyebrow>
      </div>
      <div style={{position: 'absolute', top: 190, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, ...rise(r(0.02), 14)}}>
        <span style={{fontFamily: SERIF, fontSize: 190, fontWeight: 500, color: CLAUDE.INK, lineHeight: 1}}>API Impact</span>
        <span style={{fontFamily: SERIF, fontSize: 190, fontWeight: 500, color: CLAUDE.SPARK, lineHeight: 1}}>.</span>
        <div style={{fontFamily: SERIF, fontSize: 54, fontStyle: 'italic', color: CLAUDE.INK, marginTop: 30, maxWidth: 1720, lineHeight: 1.25}}>
          Find the frontend lines your API change breaks, and fix them before you merge.
        </div>
      </div>
      <div style={{position: 'absolute', top: 640, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, height: 3, background: CLAUDE.BORDER, opacity: r(0.15)}} />
      <div style={{position: 'absolute', top: 690, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, display: 'flex', gap: 40}}>
        {facts.map((f) => (
          <div key={f.k} style={{flex: 1, ...rise(r(f.at), 10)}}>
            <Eyebrow>{f.k}</Eyebrow>
            <div style={{fontFamily: SANS, fontSize: 38, color: CLAUDE.INK, marginTop: 12, lineHeight: 1.3}}>{f.v}</div>
          </div>
        ))}
      </div>
      <div style={{position: 'absolute', bottom: 1080 - SAFE.b + 12, right: 1920 - SAFE.r + 6, fontFamily: SANS, fontSize: 24,
        color: CLAUDE.INK_SOFT, opacity: r(0.5)}}>Narration: synthetic voice (Kokoro) · script by Chethan Gowda</div>
    </Stage>
  );
};

// ── B02 · the failure (constructed) ─────────────────────────────────────────

export const AipRenameBreak: React.FC<AipProps> = ({durationSeconds, sparkLine}) => {
  const r = useReveal(durationSeconds);
  const chips = ['Tests pass', 'Merged', 'Deployed'];
  const blank = r(0.8);
  return (
    <Stage>
      <Title text="One rename. Two repos." p={r(0)} />
      <Label text="Constructed example" kind="constructed" />
      <div style={{position: 'absolute', top: 210, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, display: 'flex', gap: 60}}>
        {/* backend */}
        <Card style={{flex: 1, height: 600, ...rise(r(0.05))}}>
          <Eyebrow>Backend repo · pull request</Eyebrow>
          <div style={{fontFamily: MONO, fontSize: 34, color: CLAUDE.INK, marginTop: 28, lineHeight: 1.7}}>
            <div>Profile:</div>
            <div style={{position: 'relative', paddingLeft: 24, background: r(0.12) > 0.5 ? CLAUDE.PILL : 'transparent', opacity: 1}}>
              −  username: string
              <div style={{position: 'absolute', left: 60, top: '52%', height: 4, background: CLAUDE.SPARK,
                width: `${interpolate(r(0.12), [0, 1], [0, 330])}px`}} />
            </div>
            <div style={{paddingLeft: 24, ...rise(r(0.16), 8)}}>+  handle: string</div>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', gap: 20, marginTop: 50}}>
            {chips.map((c, i) => (
              <div key={c} style={{display: 'flex', alignItems: 'center', gap: 18, ...rise(r(0.3 + i * 0.07), 10)}}>
                <Check ok />
                <span style={{fontFamily: SANS, fontSize: 38, color: CLAUDE.INK}}>{c}</span>
              </div>
            ))}
          </div>
        </Card>
        {/* frontend */}
        <Card accent={blank > 0.5} style={{flex: 1, height: 600, ...rise(r(0.55))}}>
          <Eyebrow>Frontend repo · separate</Eyebrow>
          <div style={{fontFamily: MONO, fontSize: 34, color: CLAUDE.INK, marginTop: 28, lineHeight: 1.7}}>
            <div>&lt;h4&gt;{'{{ '}<span style={{borderBottom: `5px solid ${CLAUDE.SPARK}`}}>p.username</span>{' }}'}&lt;/h4&gt;</div>
          </div>
          {/* tiny profile page mock */}
          <div style={{marginTop: 40, border: `2px solid ${CLAUDE.BORDER}`, borderRadius: 14, padding: 28,
            display: 'flex', alignItems: 'center', gap: 30, background: CLAUDE.FOOTER}}>
            <div style={{width: 120, height: 120, borderRadius: 60, background: CLAUDE.BORDER}} />
            <div style={{flex: 1}}>
              <div style={{fontFamily: SERIF, fontSize: 48, color: CLAUDE.INK, height: 62}}>
                {blank > 0.5 ? '' : 'jake'}
              </div>
              <div style={{height: 14, width: '70%', background: CLAUDE.BORDER, borderRadius: 7, marginTop: 14}} />
            </div>
          </div>
          <div style={{fontFamily: SANS, fontSize: 34, color: CLAUDE.INK, marginTop: 30, ...rise(blank, 8)}}>
            Profile name renders blank — found after deploy.
          </div>
        </Card>
      </div>
      <Footer sparkLine={sparkLine} p={r(0.2)} />
    </Stage>
  );
};

// ── B03 · alternatives ──────────────────────────────────────────────────────

export const AipAltCompare: React.FC<AipProps> = ({durationSeconds, sparkLine}) => {
  const r = useReveal(durationSeconds);
  const cols = ['oasdiff', 'Optic', 'API Impact'];
  const rows: {label: string; cells: ('yes' | 'no' | 'will')[]; at: number}[] = [
    {label: 'Flags breaking spec changes', cells: ['yes', 'yes', 'will'], at: 0.3},
    {label: 'Runs in CI on the pull request', cells: ['yes', 'yes', 'will'], at: 0.5},
    {label: 'Names the frontend file:line that breaks', cells: ['no', 'no', 'will'], at: 0.65},
    {label: 'Opens a fix PR in the frontend repo', cells: ['no', 'no', 'will'], at: 0.78},
  ];
  const colW = 330;
  return (
    <Stage>
      <Title text="What already exists" p={r(0)} />
      <Label text="From public docs · checked 2026-10-13" kind="real" />
      <div style={{position: 'absolute', top: 220, left: SAFE.x + 6, right: 1920 - SAFE.r + 6}}>
        <div style={{display: 'flex', alignItems: 'flex-end', ...rise(r(0.1))}}>
          <div style={{flex: 1}} />
          {cols.map((c, i) => (
            <div key={c} style={{width: colW, textAlign: 'center', fontFamily: SERIF, fontSize: 50, fontWeight: 600, color: CLAUDE.INK}}>
              {c}
              {i === 2 ? <div style={{fontFamily: SANS, fontSize: 24, color: CLAUDE.INK_SOFT, fontWeight: 400}}>planned</div> : null}
            </div>
          ))}
        </div>
        {rows.map((row) => {
          const p = r(row.at);
          return (
            <div key={row.label} style={{display: 'flex', alignItems: 'center', height: 150,
              borderTop: `2px solid ${CLAUDE.BORDER}`, ...rise(p, 10)}}>
              <div style={{flex: 1, fontFamily: SANS, fontSize: 40, color: CLAUDE.INK, paddingRight: 30}}>{row.label}</div>
              {row.cells.map((cell, i) => (
                <div key={i} style={{width: colW, display: 'flex', justifyContent: 'center'}}>
                  {cell === 'yes' ? <Check ok size={56} /> : cell === 'no' ? (
                    <span style={{fontFamily: SANS, fontSize: 56, color: CLAUDE.INK_SOFT}}>—</span>
                  ) : (
                    <span style={{fontFamily: SANS, fontSize: 36, fontWeight: 700, color: CLAUDE.INK,
                      border: `3px ${row.at > 0.6 ? 'solid' : 'dashed'} ${row.at > 0.6 ? CLAUDE.SPARK : CLAUDE.BORDER}`,
                      background: row.at > 0.6 ? ACCENT_TINT : 'transparent', borderRadius: 12, padding: '6px 22px'}}>will</span>
                  )}
                </div>
              ))}
            </div>
          );
        })}
      </div>
      <Footer sparkLine={sparkLine} p={r(0.35)} />
    </Stage>
  );
};

// ── B04 · plain search noise (REAL run) ─────────────────────────────────────

const GREP_SAMPLES: {file: string; code: string; tag: string; real?: boolean}[] = [
  {file: 'auth.component.html:21', code: 'formControlName="username"', tag: 'form field'},
  {file: 'profile.routes.ts:9', code: "path: ':username',", tag: 'route param'},
  {file: 'user.service.ts:17', code: '* … /profiles/:username): …', tag: 'comment'},
  {file: 'profile.component.html:17', code: '<h4>{{ p.username }}</h4>', tag: 'reads the API response', real: true},
];

export const AipGrepNoise: React.FC<AipProps> = ({durationSeconds, sparkLine}) => {
  const r = useReveal(durationSeconds);
  const n = Math.round(interpolate(r(0.35), [0, 1], [0, 171]));
  const split = r(0.6);
  return (
    <Stage>
      <Title text="Plain search for “username”" p={r(0)} />
      <Label text="Real run · angular-realworld @ dd99ed2 · 2026-10-13" kind="real" />
      <div style={{position: 'absolute', top: 200, left: SAFE.x + 6, width: 760}}>
        <Card style={{...rise(r(0.12))}}>
          <div style={{fontFamily: MONO, fontSize: 28, color: CLAUDE.INK, lineHeight: 1.5}}>
            $ grep -rnw username src<br />&nbsp;&nbsp;--include=*.ts --include=*.html
          </div>
        </Card>
        <div style={{display: 'flex', alignItems: 'baseline', gap: 24, marginTop: 40, ...rise(r(0.3))}}>
          <span style={{fontFamily: SERIF, fontSize: 190, fontWeight: 600, color: CLAUDE.INK, lineHeight: 1}}>{n}</span>
          <span style={{fontFamily: SANS, fontSize: 40, color: CLAUDE.INK}}>matches<br />in 23 files</span>
        </div>
        <div style={{marginTop: 40, ...rise(split)}}>
          <div style={{display: 'flex', height: 64, borderRadius: 10, overflow: 'hidden', border: `2px solid ${CLAUDE.BORDER}`}}>
            <div style={{width: `${(124 / 171) * 100}%`, background: CLAUDE.BORDER}} />
            <div style={{flex: 1, background: CLAUDE.SPARK}} />
          </div>
          <div style={{display: 'flex', justifyContent: 'space-between', fontFamily: SANS, fontSize: 30, color: CLAUDE.INK, marginTop: 12}}>
            <span>124 in test files (*.spec.ts)</span><span>47 elsewhere</span>
          </div>
        </div>
      </div>
      <div style={{position: 'absolute', top: 200, left: 940, right: 1920 - SAFE.r + 6, display: 'flex', flexDirection: 'column', gap: 22}}>
        <Eyebrow style={{...rise(r(0.58))}}>Four of the 47, verbatim</Eyebrow>
        {GREP_SAMPLES.map((s, i) => (
          <Card key={s.file} accent={s.real} style={{padding: '16px 24px', ...rise(r(0.6 + i * 0.04), 10)}}>
            <div style={{fontFamily: MONO, fontSize: 22, color: CLAUDE.INK_SOFT}}>{s.file}</div>
            <div style={{fontFamily: MONO, fontSize: 28, color: CLAUDE.INK, marginTop: 4, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{s.code}</div>
            <div style={{fontFamily: SANS, fontSize: 26, fontWeight: 700, color: CLAUDE.INK, marginTop: 6}}>→ {s.tag}</div>
          </Card>
        ))}
      </div>
      <Footer sparkLine={sparkLine} p={r(0.5)} />
    </Stage>
  );
};

// ── B05 · the chain (REAL code) ─────────────────────────────────────────────

type Tok = {t: string; hot?: boolean};
const TRACE: {file: string; step: string; lines: {n: number; toks: Tok[]}[]; at: number}[] = [
  {file: 'profile.service.ts', step: 'API call → response', at: 0.1, lines: [
    {n: 19, toks: [{t: 'return this.http.get<…>('}, {t: "'/profiles/'", hot: true}, {t: ' + username).pipe('}]},
    {n: 20, toks: [{t: '  map((data) => '}, {t: 'data.profile', hot: true}, {t: '),'}]},
  ]},
  {file: 'profile.component.ts', step: 'response → variable', at: 0.35, lines: [
    {n: 54, toks: [{t: '.subscribe((['}, {t: 'profile', hot: true}, {t: ', user]) => {'}]},
    {n: 55, toks: [{t: '  this.profile.set('}, {t: 'profile', hot: true}, {t: ');'}]},
  ]},
  {file: 'profile.component.html', step: 'variable → property', at: 0.6, lines: [
    {n: 11, toks: [{t: '@if (profile(); as '}, {t: 'p', hot: true}, {t: ') {'}]},
    {n: 17, toks: [{t: '  <h4>{{ '}, {t: 'p.username', hot: true}, {t: ' }}</h4>'}]},
  ]},
];

export const AipTraceChain: React.FC<AipProps> = ({durationSeconds, sparkLine}) => {
  const r = useReveal(durationSeconds);
  const link = r(0.8);
  return (
    <Stage>
      <Title text="One real read, three files" p={r(0)} />
      <Label text="Real code · angular-realworld @ dd99ed2 (MIT)" kind="real" />
      {/* connector rail */}
      <div style={{position: 'absolute', left: SAFE.x + 30, top: 250, width: 8, borderRadius: 4,
        height: interpolate(link, [0, 1], [0, 470]), background: CLAUDE.SPARK}} />
      <div style={{position: 'absolute', top: 210, left: SAFE.x + 80, right: 1920 - SAFE.r + 6, display: 'flex', flexDirection: 'column', gap: 26}}>
        {TRACE.map((card) => {
          const p = r(card.at);
          return (
            <div key={card.file} style={{display: 'flex', gap: 30, alignItems: 'stretch', ...rise(p)}}>
              <Card style={{flex: 1, padding: '18px 28px'}}>
                <div style={{fontFamily: MONO, fontSize: 24, color: CLAUDE.INK_SOFT}}>{card.file}</div>
                {card.lines.map((ln) => (
                  <div key={ln.n} style={{fontFamily: MONO, fontSize: 32, color: CLAUDE.INK, whiteSpace: 'pre', marginTop: 6}}>
                    <span style={{color: CLAUDE.INK_SOFT, display: 'inline-block', width: 64}}>{ln.n}</span>
                    {ln.toks.map((tk, i) => (
                      <span key={i} style={tk.hot ? {borderBottom: `5px solid ${link > 0.5 ? CLAUDE.SPARK : CLAUDE.BORDER}`, fontWeight: 700} : undefined}>{tk.t}</span>
                    ))}
                  </div>
                ))}
              </Card>
              <div style={{width: 320, display: 'flex', alignItems: 'center', fontFamily: SERIF, fontSize: 38, fontStyle: 'italic', color: CLAUDE.INK}}>
                {card.step}
              </div>
            </div>
          );
        })}
      </div>
      <Footer sparkLine={sparkLine} p={r(0.85)} />
    </Stage>
  );
};

// ── B06 · the five-stage pipeline (PLANNED) ─────────────────────────────────

const STAGES = [
  {k: '1', name: 'oasdiff', desc: 'old spec vs new spec → breaking changes', at: 0.08},
  {k: '2', name: 'tree-sitter', desc: 'trace each field to where it’s read', at: 0.2},
  {k: '3', name: 'Claude', desc: 'hard cases, and the edit for each confirmed line', tag: 'fixed output format', at: 0.38},
  {k: '4', name: 'Verify', desc: 're-check every line; fix must pass tsc + tests', at: 0.56},
  {k: '5', name: 'Draft PRs', desc: 'one fix PR per frontend repo, linked to the backend PR', at: 0.7},
];

export const AipPipeline: React.FC<AipProps> = ({durationSeconds, sparkLine}) => {
  const r = useReveal(durationSeconds);
  const cardW = 300;
  return (
    <Stage>
      <Title text="How it will work" p={r(0)} />
      <Label text="Planned · nothing built yet" kind="planned" />
      <div style={{position: 'absolute', top: 250, left: SAFE.x + 6, right: 1920 - SAFE.r + 6,
        display: 'flex', justifyContent: 'space-between', alignItems: 'stretch'}}>
        {STAGES.map((s, i) => {
          const p = r(s.at);
          const focal = s.name === 'Verify';
          return (
            <React.Fragment key={s.k}>
              <Card accent={focal && p > 0.5} style={{width: cardW, height: 520, padding: '26px 24px',
                background: focal && p > 0.5 ? '#FFF8F4' : CLAUDE.CARD, ...rise(p)}}>
                <div style={{fontFamily: SANS, fontSize: 28, fontWeight: 700, color: CLAUDE.INK_SOFT}}>{s.k}</div>
                <div style={{fontFamily: SERIF, fontSize: 48, fontWeight: 600, color: CLAUDE.INK, marginTop: 6}}>{s.name}</div>
                <div style={{fontFamily: SANS, fontSize: 30, color: CLAUDE.INK, marginTop: 18, lineHeight: 1.35}}>{s.desc}</div>
                {s.tag ? (
                  <div style={{marginTop: 22, display: 'inline-block', fontFamily: MONO, fontSize: 24, color: CLAUDE.INK,
                    background: CLAUDE.PILL, borderRadius: 8, padding: '6px 12px'}}>{s.tag}</div>
                ) : null}
              </Card>
              {i < STAGES.length - 1 ? (
                <div style={{display: 'flex', alignItems: 'center', opacity: r(STAGES[i + 1].at)}}>
                  <div style={{width: 22, height: 4, background: CLAUDE.INK_SOFT}} />
                  <div style={{width: 0, height: 0, borderLeft: `14px solid ${CLAUDE.INK_SOFT}`,
                    borderTop: '10px solid transparent', borderBottom: '10px solid transparent'}} />
                </div>
              ) : null}
            </React.Fragment>
          );
        })}
      </div>
      <Footer sparkLine={sparkLine} p={r(0.3)} />
    </Stage>
  );
};

// ── B07 · the verifier (CONSTRUCTED illustration; cited lines are real) ─────

type Mark = 'yes' | 'no' | 'na';
const CANDIDATES: {file: string; kind: string; code: string; has: Mark; fix: Mark; verdict: string; at: number}[] = [
  {file: 'profile.component.html:17', kind: 'confirmed', code: '<h4>{{ p.username }}</h4>', has: 'yes', fix: 'yes', verdict: 'FIX PR', at: 0.4},
  {file: 'follow-button.component.ts:34', kind: 'possible', code: '{{ profile.username }}', has: 'yes', fix: 'na', verdict: 'LIST ONLY', at: 0.55},
  {file: 'profile.component.html:15', kind: 'cited', code: '<img [src]="p.image | defaultImage" …', has: 'no', fix: 'na', verdict: 'DROPPED', at: 0.68},
];

const MarkCell: React.FC<{m: Mark}> = ({m}) => (
  m === 'na' ? <span style={{fontFamily: SANS, fontSize: 52, color: CLAUDE.INK_SOFT}}>—</span> : <Check ok={m === 'yes'} size={52} />
);

export const AipVerifyGate: React.FC<AipProps> = ({durationSeconds, sparkLine}) => {
  const r = useReveal(durationSeconds);
  return (
    <Stage>
      <Title text="Nothing trusted on the model’s word" p={r(0)} />
      <Label text="Constructed illustration of planned behavior" kind="constructed" />
      <div style={{position: 'absolute', top: 205, left: SAFE.x + 6, right: 1920 - SAFE.r + 6}}>
        <div style={{display: 'flex', fontFamily: SANS, fontSize: 24, fontWeight: 700, letterSpacing: 2.5,
          textTransform: 'uppercase', color: CLAUDE.INK_SOFT, paddingBottom: 12, ...rise(r(0.12))}}>
          <div style={{flex: 1}}>Claude points to</div>
          <div style={{width: 260, textAlign: 'center'}}>Line has “username”</div>
          <div style={{width: 280, textAlign: 'center'}}>Fix passes tsc + tests</div>
          <div style={{width: 260, textAlign: 'center'}}>Result</div>
        </div>
        {CANDIDATES.map((c) => {
          const enter = r(0.15);
          const p = r(c.at);
          const dropped = c.verdict === 'DROPPED';
          return (
            <div key={c.file} style={{display: 'flex', alignItems: 'center', height: 190, borderTop: `2px solid ${CLAUDE.BORDER}`, ...rise(enter)}}>
              <div style={{flex: 1, opacity: dropped && p > 0.5 ? 0.55 : 1}}>
                <div style={{fontFamily: MONO, fontSize: 26, color: CLAUDE.INK_SOFT}}>{c.file} · {c.kind}</div>
                <div style={{position: 'relative', fontFamily: MONO, fontSize: 32, color: CLAUDE.INK, marginTop: 6, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: 800}}>
                  {c.code}
                  {dropped ? (
                    <div style={{position: 'absolute', left: 0, top: '44%', height: 5, background: CLAUDE.SPARK,
                      width: `${interpolate(p, [0, 1], [0, 740])}px`}} />
                  ) : null}
                </div>
              </div>
              <div style={{width: 260, display: 'flex', justifyContent: 'center', opacity: p}}><MarkCell m={c.has} /></div>
              <div style={{width: 280, display: 'flex', justifyContent: 'center', opacity: p}}><MarkCell m={c.fix} /></div>
              <div style={{width: 260, display: 'flex', justifyContent: 'center', ...rise(p, 8)}}>
                <span style={{fontFamily: SANS, fontSize: 32, fontWeight: 700, color: CLAUDE.INK,
                  border: `3px solid ${dropped ? CLAUDE.SPARK : CLAUDE.INK_SOFT}`, background: dropped ? ACCENT_TINT : 'transparent',
                  borderRadius: 10, padding: '8px 18px', whiteSpace: 'nowrap'}}>{c.verdict}</span>
              </div>
            </div>
          );
        })}
      </div>
      <Footer sparkLine={sparkLine} p={r(0.75)} />
    </Stage>
  );
};

// ── B08 · the draft fix PR (CONSTRUCTED mock-up) ───────────────────────────

export const AipPrComment: React.FC<AipProps> = ({durationSeconds, sparkLine}) => {
  const r = useReveal(durationSeconds);
  const checks = ['tsc', 'tests'];
  return (
    <Stage>
      <Title text="A draft fix, not a surprise" p={r(0)} />
      <Label text="Constructed mock-up of a v1 fix PR" kind="constructed" />
      <Card style={{position: 'absolute', top: 200, left: SAFE.x + 6, width: 1080, padding: 0, overflow: 'hidden', ...rise(r(0.05))}}>
        <div style={{background: CLAUDE.FOOTER, borderBottom: `2px solid ${CLAUDE.BORDER}`, padding: '18px 30px',
          fontFamily: SANS, fontSize: 28, color: CLAUDE.INK}}>
          <b>Draft</b> · angular-realworld-example-app <span style={{color: CLAUDE.INK_SOFT}}>(mock-up)</span>
        </div>
        <div style={{padding: '24px 30px'}}>
          <div style={{fontFamily: SANS, fontSize: 34, fontWeight: 700, color: CLAUDE.INK}}>Rename username → handle</div>
          <div style={{fontFamily: SANS, fontSize: 26, color: CLAUDE.INK_SOFT, marginTop: 8}}>Opened from the backend pull request that changed GET /profiles/{'{username}'}</div>
          <div style={{marginTop: 24, background: CLAUDE.FOOTER, borderRadius: 12, padding: '16px 22px', ...rise(r(0.2), 10)}}>
            <div style={{fontFamily: MONO, fontSize: 24, color: CLAUDE.INK_SOFT}}>…/profile/profile.component.html:17</div>
            <div style={{fontFamily: MONO, fontSize: 32, color: CLAUDE.INK, marginTop: 8}}>−  &lt;h4&gt;{'{{ p.username }}'}&lt;/h4&gt;</div>
            <div style={{fontFamily: MONO, fontSize: 32, color: CLAUDE.INK, marginTop: 4}}>
              +  &lt;h4&gt;{'{{ '}<span style={{borderBottom: `5px solid ${CLAUDE.SPARK}`}}>p.handle</span>{' }}'}&lt;/h4&gt;
            </div>
          </div>
          <div style={{display: 'flex', gap: 34, marginTop: 24, alignItems: 'center', ...rise(r(0.35), 8)}}>
            {checks.map((c) => (
              <div key={c} style={{display: 'flex', alignItems: 'center', gap: 10}}>
                <Check ok size={40} /><span style={{fontFamily: SANS, fontSize: 30, color: CLAUDE.INK}}>{c}</span>
              </div>
            ))}
            <span style={{fontFamily: SANS, fontSize: 30, color: CLAUDE.INK}}>· waiting for human review</span>
          </div>
          <div style={{marginTop: 24, marginBottom: 6, fontFamily: SANS, fontSize: 28, color: CLAUDE.INK, ...rise(r(0.55), 8)}}>
            Listed, not edited: <span style={{fontFamily: MONO, fontSize: 26}}>follow-button.component.ts:34</span> (possible)
          </div>
        </div>
      </Card>
      <div style={{position: 'absolute', top: 200, left: 1240, right: 1920 - SAFE.r + 6, display: 'flex', flexDirection: 'column', gap: 28}}>
        <Card style={{...rise(r(0.45))}}>
          <Eyebrow>Setup</Eyebrow>
          <div style={{fontFamily: SANS, fontSize: 30, color: CLAUDE.INK, marginTop: 12, lineHeight: 1.45}}>
            Config + workflow in the backend repo<br />GitHub App: PR access to frontend repos
          </div>
        </Card>
        <Card accent style={{...rise(r(0.75))}}>
          <Eyebrow>Merge</Eyebrow>
          <div style={{fontFamily: SANS, fontSize: 32, color: CLAUDE.INK, marginTop: 12, lineHeight: 1.4}}>
            Nothing auto-merges.<br />A person reviews every PR.
          </div>
        </Card>
      </div>
      <Footer sparkLine={sparkLine} p={r(0.3)} />
    </Stage>
  );
};

// ── B09 · eval design (PLANNED, no results) ─────────────────────────────────

export const AipEvalGrid: React.FC<AipProps> = ({durationSeconds, sparkLine}) => {
  const r = useReveal(durationSeconds);
  const systems = ['Plain search', 'Regen types + tsc', 'API Impact'];
  const metrics = ['Catch rate', 'False alarms', 'Citation accuracy', 'Fixes passing tests'];
  return (
    <Stage>
      <Title text="How it will be judged" p={r(0)} />
      <Label text="Planned · no results exist" kind="planned" />
      <Card style={{position: 'absolute', top: 190, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, padding: '18px 30px', ...rise(r(0.06))}}>
        <span style={{fontFamily: SANS, fontSize: 32, color: CLAUDE.INK}}>
          <b>Test bed:</b> forked RealWorld backend + frontend · ~20 planted breaking changes · + real ones from public histories
        </span>
      </Card>
      <div style={{position: 'absolute', top: 320, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, ...rise(r(0.25))}}>
        <div style={{display: 'flex'}}>
          <div style={{width: 440}} />
          {systems.map((s) => (
            <div key={s} style={{flex: 1, textAlign: 'center', fontFamily: SERIF, fontSize: 40, fontWeight: 600, color: CLAUDE.INK}}>{s}</div>
          ))}
        </div>
        {metrics.map((m, mi) => (
          <div key={m} style={{display: 'flex', alignItems: 'center', height: 92, borderTop: `2px solid ${CLAUDE.BORDER}`,
            background: mi === 3 && r(0.5) > 0.5 ? ACCENT_TINT : 'transparent', ...rise(r(mi === 3 ? 0.5 : 0.25), 8)}}>
            <div style={{width: 440, fontFamily: SANS, fontSize: 36, color: CLAUDE.INK, paddingLeft: 8}}>{m}</div>
            {systems.map((s) => (
              <div key={s} style={{flex: 1, textAlign: 'center', fontFamily: SANS, fontSize: 28, color: CLAUDE.INK_SOFT}}>
                {mi === 3 && s !== 'API Impact' ? 'n/a — no fixes' : '— no result yet'}
              </div>
            ))}
          </div>
        ))}
      </div>
      <div style={{position: 'absolute', top: 790, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, display: 'flex', flexWrap: 'wrap', gap: 18, alignItems: 'center'}}>
        <Eyebrow style={{width: '100%', ...rise(r(0.68))}}>If the numbers hold up, evidence for</Eyebrow>
        {['source grounding', 'verification', 'prompt contracts', 'evaluation'].map((c, i) => (
          <span key={c} style={{fontFamily: SANS, fontSize: 30, color: CLAUDE.INK, background: CLAUDE.PILL,
            border: `2px solid ${i === 1 ? CLAUDE.SPARK : CLAUDE.BORDER}`, borderRadius: 999, padding: '8px 24px', ...rise(r(0.7 + i * 0.03), 8)}}>{c}</span>
        ))}
        <span style={{fontFamily: SANS, fontSize: 30, color: CLAUDE.INK_SOFT, padding: '8px 24px',
          border: `2px dashed ${CLAUDE.BORDER}`, borderRadius: 999, ...rise(r(0.84), 8)}}>agent loops — not claimed</span>
      </div>
      <Footer sparkLine={sparkLine} p={r(0.45)} />
    </Stage>
  );
};

// ── B10 · scope: in / out / first (PLANNED) ─────────────────────────────────

export const AipScope: React.FC<AipProps> = ({durationSeconds, sparkLine}) => {
  const r = useReveal(durationSeconds);
  const col = (title: string, items: string[], at: number, accent = false) => (
    <Card accent={accent} style={{flex: 1, height: 600, ...rise(r(at))}}>
      <div style={{fontFamily: SERIF, fontSize: 56, fontWeight: 600, color: CLAUDE.INK}}>{title}</div>
      <div style={{height: 6, width: 90, background: accent ? CLAUDE.SPARK : CLAUDE.BORDER, borderRadius: 3, margin: '14px 0 26px'}} />
      {items.map((it, i) => (
        <div key={it} style={{fontFamily: SANS, fontSize: 34, color: CLAUDE.INK, marginBottom: 24, lineHeight: 1.3, ...rise(r(at + 0.03 * (i + 1)), 6)}}>{it}</div>
      ))}
    </Card>
  );
  const steps = ['One planted rename', '→ prints the exact file:line', '→ draft fix passes CI'];
  return (
    <Stage>
      <Title text="What v1 will and won’t do" p={r(0)} />
      <Label text="Planned" kind="planned" />
      <div style={{position: 'absolute', top: 200, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, display: 'flex', gap: 40}}>
        {col('Will handle', ['Renamed fields', 'Retyped fields', 'TypeScript frontends'], 0.04)}
        {col('Will never', ['Merge its own fixes', 'Guess at deleted fields — flags them instead', 'GraphQL (v1)'], 0.24, true)}
        <Card style={{flex: 1, height: 600, ...rise(r(0.55))}}>
          <div style={{fontFamily: SERIF, fontSize: 56, fontWeight: 600, color: CLAUDE.INK}}>Runs first</div>
          <div style={{height: 6, width: 90, background: CLAUDE.BORDER, borderRadius: 3, margin: '14px 0 26px'}} />
          {steps.map((st, i) => (
            <div key={st} style={{fontFamily: i === 0 ? SANS : MONO, fontSize: i === 0 ? 34 : 28, color: CLAUDE.INK,
              marginBottom: 24, lineHeight: 1.3, ...rise(r(0.6 + i * 0.1), 6)}}>{st}</div>
          ))}
          <div style={{display: 'flex', alignItems: 'center', gap: 14, marginTop: 10, ...rise(r(0.82), 8)}}>
            <Check ok size={44} />
            <span style={{fontFamily: SANS, fontSize: 30, color: CLAUDE.INK}}>That’s how you’ll know it ran</span>
          </div>
        </Card>
      </div>
      <Footer sparkLine={sparkLine} p={r(0.4)} />
    </Stage>
  );
};

// ── B11 · risk ──────────────────────────────────────────────────────────────

export const AipRisk: React.FC<AipProps> = ({durationSeconds, sparkLine}) => {
  const r = useReveal(durationSeconds);
  const guards = ['Only confirmed lines get edited', 'Every fix must pass tsc + tests', 'Draft PR · a person merges'];
  return (
    <Stage>
      <Title text="What could sink it" p={r(0)} />
      <Label text="Risk + plan" kind="planned" />
      <div style={{position: 'absolute', top: 200, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, display: 'flex', gap: 40}}>
        <Card accent style={{flex: 1.1, height: 600, ...rise(r(0.06))}}>
          <Eyebrow>The risk</Eyebrow>
          <div style={{fontFamily: SERIF, fontSize: 54, fontWeight: 600, color: CLAUDE.INK, marginTop: 14, lineHeight: 1.15}}>
            A fix that compiles but is wrong
          </div>
          <div style={{fontFamily: SANS, fontSize: 30, color: CLAUDE.INK, marginTop: 26, lineHeight: 1.4}}>
            e.g. a <span style={{fontFamily: MONO}}>username</span> that came from a different endpoint
          </div>
        </Card>
        <Card style={{flex: 1, height: 600, ...rise(r(0.3))}}>
          <Eyebrow>Guardrails</Eyebrow>
          {guards.map((g, i) => (
            <div key={g} style={{display: 'flex', alignItems: 'center', gap: 16, marginTop: 34, ...rise(r(0.32 + i * 0.08), 8)}}>
              <Check ok size={44} />
              <span style={{fontFamily: SANS, fontSize: 32, color: CLAUDE.INK, lineHeight: 1.3}}>{g}</span>
            </div>
          ))}
        </Card>
        <Card style={{flex: 1, height: 600, ...rise(r(0.66))}}>
          <Eyebrow>If tracing doesn’t hold up</Eyebrow>
          <div style={{fontFamily: MONO, fontSize: 26, color: CLAUDE.INK, marginTop: 18, lineHeight: 1.5}}>
            RxJS chains, generated clients
          </div>
          <div style={{fontFamily: SANS, fontSize: 36, color: CLAUDE.INK, marginTop: 26, lineHeight: 1.4}}>
            Narrow v1 to one client pattern.
          </div>
          <div style={{fontFamily: SANS, fontSize: 36, color: CLAUDE.INK, marginTop: 26, lineHeight: 1.4}}>
            Say so in the eval report.
          </div>
        </Card>
      </div>
      <Footer sparkLine={sparkLine} p={r(0.5)} />
    </Stage>
  );
};

// ── B12 · why this project ──────────────────────────────────────────────────

export const AipWhy: React.FC<AipProps> = ({durationSeconds, sparkLine}) => {
  const r = useReveal(durationSeconds);
  const fresh = ['tree-sitter', 'oasdiff', 'GitHub Actions', 'Claude structured output', 'evaluating AI code edits'];
  return (
    <Stage>
      <Title text="Why this project: a mix" p={r(0)} />
      <div style={{position: 'absolute', top: 200, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, display: 'flex', gap: 40, alignItems: 'stretch'}}>
        <Card style={{width: 600, height: 580, ...rise(r(0.08))}}>
          <Eyebrow>Already have</Eyebrow>
          <div style={{fontFamily: SERIF, fontSize: 64, fontWeight: 600, color: CLAUDE.INK, marginTop: 20}}>Angular</div>
          <div style={{fontFamily: SERIF, fontSize: 64, fontWeight: 600, color: CLAUDE.INK, marginTop: 6}}>TypeScript</div>
          <div style={{fontFamily: SANS, fontSize: 30, color: CLAUDE.INK, marginTop: 40, border: `2px dashed ${CLAUDE.BORDER}`,
            borderRadius: 12, padding: '14px 18px'}}>Experience · on GitHub</div>
        </Card>
        <div style={{display: 'flex', alignItems: 'center', ...rise(r(0.7))}}>
          <div style={{width: 60, height: 6, background: CLAUDE.SPARK}} />
          <div style={{width: 0, height: 0, borderLeft: `22px solid ${CLAUDE.SPARK}`, borderTop: '16px solid transparent', borderBottom: '16px solid transparent'}} />
        </div>
        <Card style={{flex: 1, height: 580, ...rise(r(0.3))}}>
          <Eyebrow>New to me</Eyebrow>
          <div style={{display: 'flex', flexWrap: 'wrap', gap: 22, marginTop: 26}}>
            {fresh.map((f, i) => (
              <span key={f} style={{fontFamily: SANS, fontSize: 36, color: CLAUDE.INK, background: CLAUDE.PILL,
                border: `2px solid ${CLAUDE.BORDER}`, borderRadius: 999, padding: '12px 28px', ...rise(r(0.36 + i * 0.06), 8)}}>{f}</span>
            ))}
          </div>
          <div style={{fontFamily: SERIF, fontSize: 40, fontStyle: 'italic', color: CLAUDE.INK, marginTop: 50, ...rise(r(0.7), 8)}}>
            Frontend → the backend side of the break
          </div>
        </Card>
      </div>
      <Footer sparkLine={sparkLine} p={r(0.3)} />
    </Stage>
  );
};

// ── BOUT · title restate (author's own outro; not the locked NBB card) ─────

export const AipTitleOutro: React.FC<AipOutroProps> = ({title, name, subline}) => {
  const frame = useCurrentFrame();
  const o = clamp01(interpolate(frame, [0, 14], [0, 1]));
  const m = title.match(/^([\s\S]*?)([.?!]+)$/);
  const body = m ? m[1] : title;
  const punct = m ? m[2] : '.';
  return (
    <Stage>
      <div style={{position: 'absolute', top: SAFE.y + 10, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, display: 'flex',
        justifyContent: 'space-between', fontFamily: SANS, fontSize: 26, letterSpacing: 2.5, textTransform: 'uppercase',
        fontWeight: 700, color: CLAUDE.INK_SOFT, opacity: o}}>
        <span>API Impact</span><span>2026-10-14</span>
      </div>
      <div style={{position: 'absolute', top: 300, left: 0, right: 0, textAlign: 'center', opacity: o}}>
        <span style={{fontFamily: SERIF, fontSize: 210, fontWeight: 500, color: CLAUDE.INK}}>{body}</span>
        <span style={{fontFamily: SERIF, fontSize: 210, fontWeight: 500, color: CLAUDE.SPARK}}>{punct}</span>
      </div>
      <div style={{position: 'absolute', top: 640, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, height: 3, background: CLAUDE.BORDER, opacity: o}} />
      <div style={{position: 'absolute', top: 690, left: 0, right: 0, textAlign: 'center', fontFamily: SERIF, fontSize: 64, color: CLAUDE.INK, opacity: o}}>{name}</div>
      <div style={{position: 'absolute', bottom: 1080 - SAFE.b + 14, left: SAFE.x + 6, right: 1920 - SAFE.r + 6, textAlign: 'center',
        fontFamily: SANS, fontSize: 26, color: CLAUDE.INK_SOFT, opacity: o}}>{subline}</div>
    </Stage>
  );
};
