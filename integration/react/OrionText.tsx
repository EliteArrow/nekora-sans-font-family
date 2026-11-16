// Minimal text component using the Orion presets.
import React from 'react';
import { orionStyle, OrionPlatform, OrionToken } from './orionTypography';

export interface OrionTextProps extends React.HTMLAttributes<HTMLSpanElement> {
  token: OrionToken;
  platform?: OrionPlatform;
  /** -50..100. Raise over bright video or for focused items instead of changing weight: layout does not move. */
  grade?: number;
  as?: keyof JSX.IntrinsicElements;
}

export function OrionText({ token, platform = 'tv', grade = 0, as: Tag = 'span', style, ...rest }: OrionTextProps) {
  const Any = Tag as any;
  return <Any style={{ ...orionStyle(platform, token, grade), ...style }} {...rest} />;
}

// Focus without reflow: the focused card keeps its width because only GRAD changes.
export function RowTitle({ focused, children }: { focused: boolean; children: React.ReactNode }) {
  return <OrionText token="titleL" grade={focused ? 80 : 0}>{children}</OrionText>;
}

// Playback clock: tabular figures, and the colon centres on the digits through the font's calt feature.
export function Clock({ value }: { value: string }) {
  return <OrionText token="numeric">{value}</OrionText>;
}
