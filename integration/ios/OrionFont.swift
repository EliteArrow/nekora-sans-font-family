// Orion for UIKit / SwiftUI on iOS, iPadOS and tvOS. Generated — edit tokens/orion-type-presets.json.
// Add fonts/variable/Orion-VF.ttf to the target and list it under UIAppFonts ("Fonts provided by application").
// Reference code written against the platform documentation; it has not been compiled. Feature keys need iOS / tvOS 15.
import UIKit
import SwiftUI
import CoreText

public enum OrionAxis { static let wght = 0x77676874, wdth = 0x77647468, opsz = 0x6F70737A, grad = 0x47524144 }   // four-char tags as integers

public struct OrionPreset { public let size: CGFloat, lineHeight: CGFloat, tracking: CGFloat, wght: CGFloat, wdth: CGFloat, opsz: CGFloat, grad: CGFloat, tabular: Bool }

public enum Orion {
    /// Variable instance. `grade` is added to the preset grade and never changes advance widths.
    public static func font(size: CGFloat, wght: CGFloat = 400, wdth: CGFloat = 100, opsz: CGFloat? = nil, grad: CGFloat = 0, tabular: Bool = false) -> UIFont {
        let variation: [Int: CGFloat] = [OrionAxis.wght: wght, OrionAxis.wdth: wdth, OrionAxis.opsz: min(72, max(10, opsz ?? size)), OrionAxis.grad: grad]
        var attrs: [UIFontDescriptor.AttributeName: Any] = [.name: "Orion-Regular", UIFontDescriptor.AttributeName(rawValue: kCTFontVariationAttribute as String): variation]
        if tabular {
            attrs[.featureSettings] = [[UIFontDescriptor.FeatureKey.type: kNumberSpacingType, UIFontDescriptor.FeatureKey.selector: kMonospacedNumbersSelector]]
        }
        return UIFont(descriptor: UIFontDescriptor(fontAttributes: attrs), size: size)
    }

    /// Dynamic Type: scales the preset with the user setting (iOS / iPadOS). tvOS has no Dynamic Type; use the tv presets as they are.
    public static func scaled(_ p: OrionPreset, style: UIFont.TextStyle = .body, grade: CGFloat = 0) -> UIFont {
        let base = font(size: p.size, wght: p.wght, wdth: p.wdth, opsz: p.opsz, grad: p.grad + grade, tabular: p.tabular)
        #if os(tvOS)
        return base
        #else
        return UIFontMetrics(forTextStyle: style).scaledFont(for: base)
        #endif
    }
}

public enum OrionTv {
    public static let displayXL = OrionPreset(size: 96, lineHeight: 104, tracking: -0.96, wght: 700, wdth: 100, opsz: 72, grad: 0, tabular: false)
    public static let displayL = OrionPreset(size: 72, lineHeight: 80, tracking: -0.54, wght: 700, wdth: 100, opsz: 72, grad: 0, tabular: false)
    public static let headlineL = OrionPreset(size: 56, lineHeight: 64, tracking: -0.28, wght: 600, wdth: 100, opsz: 56, grad: 0, tabular: false)
    public static let headlineM = OrionPreset(size: 44, lineHeight: 52, tracking: -0.11, wght: 600, wdth: 100, opsz: 44, grad: 0, tabular: false)
    public static let titleL = OrionPreset(size: 36, lineHeight: 44, tracking: 0, wght: 500, wdth: 100, opsz: 36, grad: 0, tabular: false)
    public static let titleM = OrionPreset(size: 32, lineHeight: 40, tracking: 0, wght: 600, wdth: 100, opsz: 32, grad: 0, tabular: false)
    public static let bodyL = OrionPreset(size: 30, lineHeight: 42, tracking: 0, wght: 400, wdth: 100, opsz: 28, grad: 0, tabular: false)
    public static let bodyM = OrionPreset(size: 28, lineHeight: 40, tracking: 0.14, wght: 400, wdth: 100, opsz: 26, grad: 0, tabular: false)
    public static let labelL = OrionPreset(size: 30, lineHeight: 36, tracking: 0.15, wght: 500, wdth: 100, opsz: 28, grad: 0, tabular: false)
    public static let labelM = OrionPreset(size: 28, lineHeight: 32, tracking: 0.28, wght: 600, wdth: 100, opsz: 26, grad: 0, tabular: false)
    public static let caption = OrionPreset(size: 24, lineHeight: 32, tracking: 0.24, wght: 400, wdth: 100, opsz: 20, grad: 0, tabular: false)
    public static let metadata = OrionPreset(size: 24, lineHeight: 32, tracking: 0.24, wght: 500, wdth: 100, opsz: 20, grad: 0, tabular: true)
    public static let numeric = OrionPreset(size: 28, lineHeight: 32, tracking: 0, wght: 500, wdth: 100, opsz: 24, grad: 0, tabular: true)
    public static let subtitle = OrionPreset(size: 46, lineHeight: 58, tracking: 0, wght: 500, wdth: 100, opsz: 40, grad: 40, tabular: false)
}

public enum OrionTablet {
    public static let displayXL = OrionPreset(size: 56, lineHeight: 62, tracking: -0.56, wght: 700, wdth: 100, opsz: 56, grad: 0, tabular: false)
    public static let displayL = OrionPreset(size: 44, lineHeight: 48, tracking: -0.33, wght: 700, wdth: 100, opsz: 44, grad: 0, tabular: false)
    public static let headlineL = OrionPreset(size: 34, lineHeight: 40, tracking: -0.17, wght: 600, wdth: 100, opsz: 34, grad: 0, tabular: false)
    public static let headlineM = OrionPreset(size: 28, lineHeight: 34, tracking: 0, wght: 600, wdth: 100, opsz: 28, grad: 0, tabular: false)
    public static let titleL = OrionPreset(size: 22, lineHeight: 28, tracking: 0, wght: 600, wdth: 100, opsz: 22, grad: 0, tabular: false)
    public static let titleM = OrionPreset(size: 20, lineHeight: 26, tracking: 0, wght: 600, wdth: 100, opsz: 20, grad: 0, tabular: false)
    public static let bodyL = OrionPreset(size: 18, lineHeight: 26, tracking: 0, wght: 400, wdth: 100, opsz: 18, grad: 0, tabular: false)
    public static let bodyM = OrionPreset(size: 16, lineHeight: 24, tracking: 0, wght: 400, wdth: 100, opsz: 16, grad: 0, tabular: false)
    public static let labelL = OrionPreset(size: 16, lineHeight: 20, tracking: 0, wght: 500, wdth: 100, opsz: 16, grad: 0, tabular: false)
    public static let labelM = OrionPreset(size: 15, lineHeight: 20, tracking: 0.15, wght: 600, wdth: 100, opsz: 15, grad: 0, tabular: false)
    public static let caption = OrionPreset(size: 13, lineHeight: 18, tracking: 0.13, wght: 400, wdth: 100, opsz: 13, grad: 0, tabular: false)
    public static let metadata = OrionPreset(size: 13, lineHeight: 18, tracking: 0.13, wght: 500, wdth: 100, opsz: 13, grad: 0, tabular: true)
    public static let numeric = OrionPreset(size: 15, lineHeight: 20, tracking: 0, wght: 500, wdth: 100, opsz: 15, grad: 0, tabular: true)
    public static let subtitle = OrionPreset(size: 24, lineHeight: 32, tracking: 0, wght: 500, wdth: 100, opsz: 24, grad: 40, tabular: false)
}

public enum OrionMobile {
    public static let displayXL = OrionPreset(size: 40, lineHeight: 44, tracking: -0.4, wght: 700, wdth: 100, opsz: 40, grad: 0, tabular: false)
    public static let displayL = OrionPreset(size: 34, lineHeight: 40, tracking: -0.255, wght: 700, wdth: 100, opsz: 34, grad: 0, tabular: false)
    public static let headlineL = OrionPreset(size: 28, lineHeight: 34, tracking: -0.14, wght: 700, wdth: 100, opsz: 28, grad: 0, tabular: false)
    public static let headlineM = OrionPreset(size: 24, lineHeight: 30, tracking: 0, wght: 600, wdth: 100, opsz: 24, grad: 0, tabular: false)
    public static let titleL = OrionPreset(size: 20, lineHeight: 26, tracking: 0, wght: 600, wdth: 100, opsz: 20, grad: 0, tabular: false)
    public static let titleM = OrionPreset(size: 18, lineHeight: 24, tracking: 0, wght: 600, wdth: 100, opsz: 18, grad: 0, tabular: false)
    public static let bodyL = OrionPreset(size: 17, lineHeight: 24, tracking: 0, wght: 400, wdth: 100, opsz: 17, grad: 0, tabular: false)
    public static let bodyM = OrionPreset(size: 15, lineHeight: 22, tracking: 0, wght: 400, wdth: 100, opsz: 15, grad: 0, tabular: false)
    public static let labelL = OrionPreset(size: 15, lineHeight: 20, tracking: 0, wght: 500, wdth: 100, opsz: 15, grad: 0, tabular: false)
    public static let labelM = OrionPreset(size: 14, lineHeight: 18, tracking: 0.14, wght: 600, wdth: 100, opsz: 14, grad: 0, tabular: false)
    public static let caption = OrionPreset(size: 12, lineHeight: 16, tracking: 0.18, wght: 400, wdth: 100, opsz: 12, grad: 0, tabular: false)
    public static let metadata = OrionPreset(size: 12, lineHeight: 16, tracking: 0.18, wght: 500, wdth: 100, opsz: 12, grad: 0, tabular: true)
    public static let numeric = OrionPreset(size: 13, lineHeight: 16, tracking: 0, wght: 500, wdth: 100, opsz: 13, grad: 0, tabular: true)
    public static let subtitle = OrionPreset(size: 16, lineHeight: 22, tracking: 0, wght: 500, wdth: 100, opsz: 16, grad: 40, tabular: false)
}

public extension Text {
    /// SwiftUI: `Text("Continue Watching").orion(OrionTv.headlineM)`
    func orion(_ p: OrionPreset, grade: CGFloat = 0) -> some View {
        self.font(Font(Orion.scaled(p, grade: grade))).tracking(p.tracking).lineSpacing(p.lineHeight - p.size * 1.25)
    }
}
