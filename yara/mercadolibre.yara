rule detect_mercadolibre {
    strings:
        $plain_text = "mercadolibre" ascii wide
        $base64_text = "bWVyY2Fkb2xpYnJl" nocase

    condition:
        any of them
}
