// Orion for Jetpack Compose (phone, tablet, Android TV, Fire TV). Generated — edit tokens/orion-type-presets.json.
// Variable axes need API 26+. On API < 26 Compose falls back to the static files listed in res/font/orion.xml.
package com.example.orion

import android.os.Build
import androidx.compose.ui.text.ExperimentalTextApi
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontVariation
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.em
import androidx.compose.ui.unit.sp

object OrionFont {
    private val static = FontFamily(
        Font(R.font.orion_light, FontWeight.Light), Font(R.font.orion_regular, FontWeight.Normal), Font(R.font.orion_medium, FontWeight.Medium),
        Font(R.font.orion_semibold, FontWeight.SemiBold), Font(R.font.orion_bold, FontWeight.Bold), Font(R.font.orion_black, FontWeight.Black))

    @OptIn(ExperimentalTextApi::class)
    fun variable(weight: Int, width: Float = 100f, opticalSize: Float = 14f, grade: Int = 0): FontFamily =
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) FontFamily(
            Font(R.font.orion_vf, weight = FontWeight(weight), variationSettings = FontVariation.Settings(
                FontVariation.weight(weight), FontVariation.width(width),
                FontVariation.Setting("opsz", opticalSize), FontVariation.grade(grade))))
        else static
}

/** Android TV / Fire TV: values are sp on a 960x540 dp canvas (= px / 2 at 1080p) */
object OrionTvType {
    val displayXL = TextStyle(fontFamily = OrionFont.variable(weight = 700, width = 100f, opticalSize = 72f, grade = 0),
        fontSize = 48.sp, lineHeight = 52.sp, letterSpacing = -0.01.em)
    val displayL = TextStyle(fontFamily = OrionFont.variable(weight = 700, width = 100f, opticalSize = 72f, grade = 0),
        fontSize = 36.sp, lineHeight = 40.sp, letterSpacing = -0.0075.em)
    val headlineL = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 56f, grade = 0),
        fontSize = 28.sp, lineHeight = 32.sp, letterSpacing = -0.005.em)
    val headlineM = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 44f, grade = 0),
        fontSize = 22.sp, lineHeight = 26.sp, letterSpacing = -0.0025.em)
    val titleL = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 36f, grade = 0),
        fontSize = 18.sp, lineHeight = 22.sp, letterSpacing = 0.em)
    val titleM = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 32f, grade = 0),
        fontSize = 16.sp, lineHeight = 20.sp, letterSpacing = 0.em)
    val bodyL = TextStyle(fontFamily = OrionFont.variable(weight = 400, width = 100f, opticalSize = 28f, grade = 0),
        fontSize = 15.sp, lineHeight = 21.sp, letterSpacing = 0.em)
    val bodyM = TextStyle(fontFamily = OrionFont.variable(weight = 400, width = 100f, opticalSize = 26f, grade = 0),
        fontSize = 14.sp, lineHeight = 20.sp, letterSpacing = 0.005.em)
    val labelL = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 28f, grade = 0),
        fontSize = 15.sp, lineHeight = 18.sp, letterSpacing = 0.005.em)
    val labelM = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 26f, grade = 0),
        fontSize = 14.sp, lineHeight = 16.sp, letterSpacing = 0.01.em)
    val caption = TextStyle(fontFamily = OrionFont.variable(weight = 400, width = 100f, opticalSize = 20f, grade = 0),
        fontSize = 12.sp, lineHeight = 16.sp, letterSpacing = 0.01.em)
    val metadata = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 20f, grade = 0),
        fontSize = 12.sp, lineHeight = 16.sp, letterSpacing = 0.01.em, fontFeatureSettings = "tnum")
    val numeric = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 24f, grade = 0),
        fontSize = 14.sp, lineHeight = 16.sp, letterSpacing = 0.em, fontFeatureSettings = "tnum")
    val subtitle = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 40f, grade = 40),
        fontSize = 23.sp, lineHeight = 29.sp, letterSpacing = 0.em)
}

/** phones */
object OrionMobileType {
    val displayXL = TextStyle(fontFamily = OrionFont.variable(weight = 700, width = 100f, opticalSize = 40f, grade = 0),
        fontSize = 40.sp, lineHeight = 44.sp, letterSpacing = -0.01.em)
    val displayL = TextStyle(fontFamily = OrionFont.variable(weight = 700, width = 100f, opticalSize = 34f, grade = 0),
        fontSize = 34.sp, lineHeight = 40.sp, letterSpacing = -0.0075.em)
    val headlineL = TextStyle(fontFamily = OrionFont.variable(weight = 700, width = 100f, opticalSize = 28f, grade = 0),
        fontSize = 28.sp, lineHeight = 34.sp, letterSpacing = -0.005.em)
    val headlineM = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 24f, grade = 0),
        fontSize = 24.sp, lineHeight = 30.sp, letterSpacing = 0.em)
    val titleL = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 20f, grade = 0),
        fontSize = 20.sp, lineHeight = 26.sp, letterSpacing = 0.em)
    val titleM = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 18f, grade = 0),
        fontSize = 18.sp, lineHeight = 24.sp, letterSpacing = 0.em)
    val bodyL = TextStyle(fontFamily = OrionFont.variable(weight = 400, width = 100f, opticalSize = 17f, grade = 0),
        fontSize = 17.sp, lineHeight = 24.sp, letterSpacing = 0.em)
    val bodyM = TextStyle(fontFamily = OrionFont.variable(weight = 400, width = 100f, opticalSize = 15f, grade = 0),
        fontSize = 15.sp, lineHeight = 22.sp, letterSpacing = 0.em)
    val labelL = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 15f, grade = 0),
        fontSize = 15.sp, lineHeight = 20.sp, letterSpacing = 0.em)
    val labelM = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 14f, grade = 0),
        fontSize = 14.sp, lineHeight = 18.sp, letterSpacing = 0.01.em)
    val caption = TextStyle(fontFamily = OrionFont.variable(weight = 400, width = 100f, opticalSize = 12f, grade = 0),
        fontSize = 12.sp, lineHeight = 16.sp, letterSpacing = 0.015.em)
    val metadata = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 12f, grade = 0),
        fontSize = 12.sp, lineHeight = 16.sp, letterSpacing = 0.015.em, fontFeatureSettings = "tnum")
    val numeric = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 13f, grade = 0),
        fontSize = 13.sp, lineHeight = 16.sp, letterSpacing = 0.em, fontFeatureSettings = "tnum")
    val subtitle = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 16f, grade = 40),
        fontSize = 16.sp, lineHeight = 22.sp, letterSpacing = 0.em)
}

/** tablets */
object OrionTabletType {
    val displayXL = TextStyle(fontFamily = OrionFont.variable(weight = 700, width = 100f, opticalSize = 56f, grade = 0),
        fontSize = 56.sp, lineHeight = 62.sp, letterSpacing = -0.01.em)
    val displayL = TextStyle(fontFamily = OrionFont.variable(weight = 700, width = 100f, opticalSize = 44f, grade = 0),
        fontSize = 44.sp, lineHeight = 48.sp, letterSpacing = -0.0075.em)
    val headlineL = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 34f, grade = 0),
        fontSize = 34.sp, lineHeight = 40.sp, letterSpacing = -0.005.em)
    val headlineM = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 28f, grade = 0),
        fontSize = 28.sp, lineHeight = 34.sp, letterSpacing = 0.em)
    val titleL = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 22f, grade = 0),
        fontSize = 22.sp, lineHeight = 28.sp, letterSpacing = 0.em)
    val titleM = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 20f, grade = 0),
        fontSize = 20.sp, lineHeight = 26.sp, letterSpacing = 0.em)
    val bodyL = TextStyle(fontFamily = OrionFont.variable(weight = 400, width = 100f, opticalSize = 18f, grade = 0),
        fontSize = 18.sp, lineHeight = 26.sp, letterSpacing = 0.em)
    val bodyM = TextStyle(fontFamily = OrionFont.variable(weight = 400, width = 100f, opticalSize = 16f, grade = 0),
        fontSize = 16.sp, lineHeight = 24.sp, letterSpacing = 0.em)
    val labelL = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 16f, grade = 0),
        fontSize = 16.sp, lineHeight = 20.sp, letterSpacing = 0.em)
    val labelM = TextStyle(fontFamily = OrionFont.variable(weight = 600, width = 100f, opticalSize = 15f, grade = 0),
        fontSize = 15.sp, lineHeight = 20.sp, letterSpacing = 0.01.em)
    val caption = TextStyle(fontFamily = OrionFont.variable(weight = 400, width = 100f, opticalSize = 13f, grade = 0),
        fontSize = 13.sp, lineHeight = 18.sp, letterSpacing = 0.01.em)
    val metadata = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 13f, grade = 0),
        fontSize = 13.sp, lineHeight = 18.sp, letterSpacing = 0.01.em, fontFeatureSettings = "tnum")
    val numeric = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 15f, grade = 0),
        fontSize = 15.sp, lineHeight = 20.sp, letterSpacing = 0.em, fontFeatureSettings = "tnum")
    val subtitle = TextStyle(fontFamily = OrionFont.variable(weight = 500, width = 100f, opticalSize = 24f, grade = 40),
        fontSize = 24.sp, lineHeight = 32.sp, letterSpacing = 0.em)
}
