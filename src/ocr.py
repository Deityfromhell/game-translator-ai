import easyocr


class OCRReader:
    def __init__(self, languages=None):
        if languages is None:
            languages = ["en"]

        print("Loading OCR model...")

        self.reader = easyocr.Reader(
            languages,
            gpu=False,
        )

        print("OCR model ready.")

    def read_text(self, frame):
        results = self.reader.readtext(
            frame,
            detail=0,
            paragraph=True,
        )

        return " ".join(results).strip()