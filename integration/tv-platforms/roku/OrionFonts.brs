' Orion on Roku (SceneGraph). Roku loads packaged TrueType / OpenType files through the Font node.
' It exposes no variable-axis or OpenType-feature controls, so ship static files:
'   pkg:/fonts/Orion-Regular.ttf, Orion-Medium.ttf, Orion-SemiBold.ttf, Orion-Bold.ttf   (fonts/static/Orion)
'   pkg:/fonts/OrionDisplay-Bold.ttf, OrionDisplay-SemiBold.ttf                          (fonts/static/OrionDisplay)
' Sizes below are for an FHD (1920x1080) manifest: ui_resolutions=fhd. For HD manifests multiply by 0.667.

function OrionFont(token as string) as object
    presets = {
        displayXL: { uri: "pkg:/fonts/OrionDisplay-Bold.ttf", size: 96, lineHeight: 104 }
        displayL: { uri: "pkg:/fonts/OrionDisplay-Bold.ttf", size: 72, lineHeight: 80 }
        headlineL: { uri: "pkg:/fonts/OrionDisplay-SemiBold.ttf", size: 56, lineHeight: 64 }
        headlineM: { uri: "pkg:/fonts/OrionDisplay-SemiBold.ttf", size: 44, lineHeight: 52 }
        titleL: { uri: "pkg:/fonts/Orion-Medium.ttf", size: 36, lineHeight: 44 }
        titleM: { uri: "pkg:/fonts/Orion-SemiBold.ttf", size: 32, lineHeight: 40 }
        bodyL: { uri: "pkg:/fonts/Orion-Regular.ttf", size: 30, lineHeight: 42 }
        bodyM: { uri: "pkg:/fonts/Orion-Regular.ttf", size: 28, lineHeight: 40 }
        labelL: { uri: "pkg:/fonts/Orion-Medium.ttf", size: 30, lineHeight: 36 }
        labelM: { uri: "pkg:/fonts/Orion-SemiBold.ttf", size: 28, lineHeight: 32 }
        caption: { uri: "pkg:/fonts/Orion-Regular.ttf", size: 24, lineHeight: 32 }
        metadata: { uri: "pkg:/fonts/Orion-Medium.ttf", size: 24, lineHeight: 32 }
        numeric: { uri: "pkg:/fonts/Orion-Medium.ttf", size: 28, lineHeight: 32 }
        subtitle: { uri: "pkg:/fonts/Orion-Medium.ttf", size: 46, lineHeight: 58 }
    }
    p = presets[token]
    font = CreateObject("roSGNode", "Font")
    font.uri = p.uri
    font.size = p.size
    return font
end function

' usage:  m.title.font = OrionFont("headlineM")
' Timers: Roku cannot switch on tnum, so the proportional figures are used; reserve the box width for the widest value
' (all Orion figures except 1 share one advance) or draw timers with a tabular build made by `pyftfeatfreeze`-style baking.
