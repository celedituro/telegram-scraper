rule DetectMercadoLibre {
    strings:
        $plaintext = "mercadolibre"
        $base64_encoded = { 6D 65 72 63 61 64 6F 6C 69 62 72 65 }

    condition:
        $plaintext or $base64_encoded
}
