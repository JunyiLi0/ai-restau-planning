from pathlib import Path
import pdfplumber


class PDFParser:
    def extract_text(self, pdf_path: Path) -> str:
        text_content = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)

        return "\n\n".join(text_content)

    def extract_tables(self, pdf_path: Path) -> list[list[list[str]]]:
        tables = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)

        return tables

    def extract_all(self, pdf_path: Path) -> dict:
        return {
            "text": self.extract_text(pdf_path),
            "tables": self.extract_tables(pdf_path),
        }


pdf_parser = PDFParser()
