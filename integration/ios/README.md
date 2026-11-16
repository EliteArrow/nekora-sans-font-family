# Orion on iOS, iPadOS and tvOS

1. Add `fonts/variable/Orion-VF.ttf` to the app target; add it to `UIAppFonts` in Info.plist.
2. Use `OrionFont.swift`: `Orion.font(size:wght:wdth:opsz:grad:)` builds a Core Text variation instance;
   `OrionMobile`, `OrionTablet` and `OrionTv` hold the presets.
3. Optical size is not applied automatically for custom fonts: the helper sets `opsz` from the point size.
4. tvOS: values are points on the 1920 x 1080 canvas. Focus: raise `grade` by 60-80 on the focused item instead of
   switching weight, so focus engine animations do not reflow titles.
5. If you must support a system that refuses the variable file, bundle `fonts/static/Orion/*.ttf` and
   `fonts/static/OrionDisplay/*.ttf` and select by PostScript name (`Orion-SemiBold`, `OrionDisplay-Bold`, ...).

Not verified on Apple hardware in this build — see QA-REPORT.md.
