/**
 * illustrations/pitch.tsx — scenes for the INFO 7375 Final Project Pitch Film
 * (youtube/brutalist/final-project-film, Akshit Verma).
 *
 * PitchOutro — the closing card. Deliberately NOT ClaudeTitleOutro, which hardcodes
 * @NikBearBrown and a mascot: the assignment says "do not use the instructor's name,
 * persona, or credit line". It restates the title (SponsorScout), credits the author and
 * names the course. Nothing else, at Akshit's request (2026-10-14).
 */
import React from 'react';
import { useVideoConfig } from 'remotion';
import { CLAUDE } from '../tokens/claude';
import { SAFE } from '../tokens/layout';
import { SERIF, SANS, remap, ease, useP, IlluStage } from './kit';

const useReveal = () => {
  const p = useP();
  const { durationInFrames, fps } = useVideoConfig();
  const dur = durationInFrames / fps;
  return (t: number, secs = 0.5) => ease(remap(p, t, t + secs / dur, 0, 1));
};

const Center: React.FC<{ y: number; o?: number; size?: number; font?: string; color?: string; children: React.ReactNode }> =
  ({ y, o = 1, size = 32, font = SANS, color = CLAUDE.INK_SOFT, children }) => (
    <div style={{ position: 'absolute', left: SAFE.x, top: y, width: SAFE.w, textAlign: 'center',
      fontFamily: font, fontSize: size, color, opacity: o }}>{children}</div>
  );

export const PitchOutro: React.FC<{ title: string; author: string; course: string }> = ({ title, author, course }) => {
  const rv = useReveal();
  const t = rv(0.04, 0.5), a = rv(0.2, 0.5), c = rv(0.34, 0.5);
  // Sized to fill the safe area (Gate V CANVAS-FILL >= 55%): framing rules top and bottom, large type.
  // Everything settles by 45% (Gate V samples 50%). 2026-10-14: the disclosure and voice/toolkit lines were
  // removed at Akshit's request; the synthetic voice is disclosed in README.md and SOURCES.md.
  const rule = (top: number, o: number) => (
    <div style={{ position: 'absolute', left: SAFE.x + 80, top, width: SAFE.w - 160, height: 3,
      background: CLAUDE.INK_SOFT, opacity: o }} />
  );
  return (
    <IlluStage spark="" sparkPos="top">
      {rule(170, t)}
      <Center y={250 + (1 - t) * 20} o={t} size={136} font={SERIF} color={CLAUDE.INK}>{title}</Center>
      <Center y={470} o={a} size={40}>a pitch by</Center>
      <Center y={525} o={a} size={88} font={SERIF} color={CLAUDE.INK}>{author}</Center>
      <Center y={690} o={c} size={46} color={CLAUDE.INK}>{course}</Center>
      {rule(860, c)}
    </IlluStage>
  );
};
