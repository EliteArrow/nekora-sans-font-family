# -*- coding: utf-8 -*-
"""Test corpus: OTT interface strings, language samples and punctuation / numeral stress strings."""
OTT_LIST = ['Continue Watching', 'Watch Now', 'Play from Beginning', 'Skip Intro', 'Next Episode', 'Season 01 — Episode 08',
            'New & Popular', 'Top 10 in Your Country', 'Recommended for You', '4K UHD • HDR • Dolby Atmos', '2h 35m remaining',
            '00:59:48', 'TV-MA', 'SUBTITLES & AUDIO', 'Search Movies, Shows & More', '₹1,499', '€19.99', 'R$ 39,90', 'İstanbul',
            'Łódź', 'Đặng', 'Україна', 'Ελληνικά']
OTT_STRINGS = {('ott%02d' % i): s for i, s in enumerate(OTT_LIST)}

LANGUAGE_SAMPLES = {
 'English': 'Because you watched this, we think you’ll love these. Resume playback, add to My List, or rate this title.',
 'Spanish': 'Seguir viendo · ¿Quieres continuar? El pingüino Wenceslao hizo kilómetros bajo exhaustiva lluvia y frío; añoraba a su querido cachorro.',
 'French': 'Reprendre la lecture · Dès Noël où un zéphyr haï me vêt de glaçons würmiens, je dîne d’exquis rôtis de bœuf au kir à l’aÿ d’âge mûr & cætera !',
 'German': 'Weiterschauen · Zwölf Boxkämpfer jagen Viktor quer über den großen Sylter Deich. Fußballübertragung, Staffel 2, Größe, STRASSE / STRAẞE.',
 'Italian': 'Continua a guardare · Quel vituperabile xenofobo zelante assaggia il whisky ed esclama: alleluja! Perché, più, così, è, città.',
 'Portuguese': 'Continuar assistindo · À noite, vovô Kowalsky vê o ímã cair no pé do pingüim queixoso e vovó põe açúcar no chá de tâmaras do jabuti feliz. Ação, coração, não.',
 'Dutch': 'Verder kijken · Pa’s wĳze lynx bezag vroom het fikse aquaduct. Dĳk, ĳsvrĳ, IJsselmeer, één, coördinatie, reünie, ’s avonds.',
 'Polish': 'Oglądaj dalej · Pchnąć w tę łódź jeża lub ośm skrzyń fig. Zażółć gęślą jaźń. ĄĆĘŁŃÓŚŹŻ ąćęłńóśźż.',
 'Czech': 'Pokračovat ve sledování · Příliš žluťoučký kůň úpěl ďábelské ódy. ŘŠŽČĎŤŇĚŮ řšžčďťňěů.',
 'Slovak': 'Pokračovať v pozeraní · Kŕdeľ šťastných ďatľov učí pri ústí Váhu mĺkveho koňa obhrýzať kôru a žrať čerstvé mäso. Ľ ľ Ĺ ĺ Ŕ ŕ Ô ô Ä ä.',
 'Hungarian': 'Megtekintés folytatása · Árvíztűrő tükörfúrógép. ŐŰ őű ÁÉÍÓÖÚÜ áéíóöúü.',
 'Romanian': 'Continuă vizionarea · Muzicologă în bej vând whisky și tequila, preț fix. Ș ș Ț ț Ă ă Â â Î î.',
 'Turkish': 'İzlemeye devam et · Pijamalı hasta yağız şoföre çabucak güvendi. İstanbul, ışık, IĞDIR, ığdır, Ç ç Ğ ğ Ö ö Ş ş Ü ü.',
 'Vietnamese': 'Tiếp tục xem · Do bạch kim rất quý nên sẽ dùng để lắp vô xương. Đặng, Nguyễn, Trường, Phượng, Hữu, Ơ ơ Ư ư, ẮẰẲẴẶ ắằẳẵặ ẤẦẨẪẬ ấầẩẫậ ỐỒỔỖỘ ốồổỗộ ỚỜỞỠỢ ớờởỡợ ỨỪỬỮỰ ứừửữự.',
 'Greek': 'Συνέχεια παρακολούθησης · Ξεσκεπάζω την ψυχοφθόρα βδελυγμία. Ταχίστη αλώπηξ βαφής ψημένη γη, δρασκελίζει υπέρ νωθρού κυνός. ΆΈΉΊΌΎΏ άέήίόύώ ϊϋΐΰ ς.',
 'Russian': 'Продолжить просмотр · Съешь же ещё этих мягких французских булок, да выпей чаю. В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!',
 'Ukrainian': 'Продовжити перегляд · Жебракують філософи при ґанку церкви в Гадячі, ще й шатро їхнє п’яне знаємо. Україна, їжак, Є є І і Ї ї Ґ ґ.',
 'Bulgarian': 'Продължи гледането · Жълтата дюля беше щастлива, че пухът, който цъфна, замръзна като гьон. Ъ ъ Ь ь Щ щ.',
 'Serbian': 'Настави гледање · Љубазни фењерџија чађавог лица хоће да ми покаже штос. Ђ ђ Ј ј Љ љ Њ њ Ћ ћ Џ џ. Nastavi gledanje · Ljubazni fenjerdžija čađavog lica hoće da mi pokaže štos.',
 'Swedish/Danish/Norwegian': 'Fortsätt titta · Flygande bäckasiner söka hwila på mjuka tuvor. Høj bly gom vandt fræk sexquiz på wc. Å å Æ æ Ø ø.',
 'Baltic': 'Glāžšķūņa rūķīši dzērumā čiepj Baha koncertflīģeļu vākus. Įlinkdama fechtuotojo špaga sublykčiojusi pragręžė apvalų arbūzą. Ģ ģ Ķ ķ Ļ ļ Ņ ņ Ų ų Ė ė.',
}

PUNCT_NUM_SAMPLES = {
 'punct': '“Quote” ‘single’ „low“ «guillemets» ‹single› — – - _ … · • ¡¿ !? (parens) [brackets] {braces} / \\ | ¦ * † ‡ § ¶ @ & # % ‰ ′ ″ ° ª º',
 'currency': '$ ¢ £ ¥ € ₹ ₽ ₩ ₺ ₴ ₦ ₫ ₪ ₱ ₸ ₿ ƒ ¤ ₼',
 'math': '+ − × ÷ = ≠ < > ≤ ≥ ± ≈ ~ ^ ¬ ∞ √ ∑ ∏ ∫ ∂ ∆ ◊ µ π Ω',
 'numerals': '0123456789 00:00:00 23:59:59 1,234,567.89 1.234.567,89 4K 8K 1080p 60fps 5.1 7.1.4 ¼ ½ ¾ ⅓ ⅔ ⅛ ⅜ ⅝ ⅞ ¹²³ ⁴⁵⁶⁷⁸⁹⁰ ₀₁₂₃₄₅₆₇₈₉ 16:9 21:9 № 5',
 'symbols': '← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↵ ↩ ↪ ⇤ ⇥ ⇧ ⌫ ␣ ▲ ▼ ◀ ▶ ▴ ▾ ◂ ▸ ● ○ ■ □ ◆ ★ ☆ ✓ ✕ © ® ™ ℗',
 'confusables': 'Il1| O0o S5 B8 6 9 rn m cl d vv w c e nn m I l 1 | i j ı ȷ',
 'metadata': '2024 • 2h 35m • TV-MA • 16+ • HD • 5.1 • CC • AD — S1:E8 “The Long Night” (58m) ★ 8.7/10 · 98% Match',
}
