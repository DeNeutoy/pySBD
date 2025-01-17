import pytest
import pysbd
from pysbd.utils import TextSpan


def test_no_input(pysbd_default_en_no_clean_no_span_fixture, text=""):
    segments = pysbd_default_en_no_clean_no_span_fixture.segment(text)
    assert segments == []

def test_none_input(pysbd_default_en_no_clean_no_span_fixture, text=None):
    segments = pysbd_default_en_no_clean_no_span_fixture.segment(text)
    assert segments == []

def test_newline_input(pysbd_default_en_no_clean_no_span_fixture, text="\n"):
    segments = pysbd_default_en_no_clean_no_span_fixture.segment(text)
    assert segments == []

def test_segmenter_doesnt_mutate_input(pysbd_default_en_no_clean_no_span_fixture,
                                       text='My name is Jonas E. Smith. Please turn to p. 55.'):
    segments = pysbd_default_en_no_clean_no_span_fixture.segment(text)
    assert text == 'My name is Jonas E. Smith. Please turn to p. 55.'

@pytest.mark.parametrize('text,expected',
                         [('My name is Jonas E. Smith. Please turn to p. 55.',
                            [
                                ('My name is Jonas E. Smith. ', 0, 26),
                                ('Please turn to p. 55.', 27, 48),
                            ])
                         ])
def test_sbd_char_span(en_no_clean_with_span_fixture, text, expected):
    """Test sentences with character offsets"""
    segments = en_no_clean_with_span_fixture.segment(text)
    expected_text_spans = [TextSpan(sent_w_span[0], sent_w_span[1], sent_w_span[2])
                           for sent_w_span in expected]
    assert segments == expected_text_spans
    # clubbing sentences and matching with original text
    assert text == "".join([seg.sent for seg in segments])

def test_exception_with_both_clean_and_span_true():
    """Test to not allow clean=True and char_span=True
    """
    with pytest.raises(ValueError) as e:
        seg = pysbd.Segmenter(language="en", clean=True, char_span=True)
        text = "<h2 class=\"lined\">Hello</h2>\n<p>This is a test. Another test.</p>"
        seg.segment(text)
    assert str(e.value) == "char_span must be False if clean is True. "\
                            "Since `clean=True` will modify original text."

PDF_TEST_DATA = [
    ("This is a sentence\ncut off in the middle because pdf.",
        ["This is a sentence cut off in the middle because pdf."]),
    ("Organising your care early \nmeans you'll have months to build a good relationship with your midwife or doctor, ready for \nthe birth.",
        ["Organising your care early means you'll have months to build a good relationship with your midwife or doctor, ready for the birth."]),
    ("10. Get some rest \n \nYou have the best chance of having a problem-free pregnancy and a healthy baby if you follow \na few simple guidelines:",
        ["10. Get some rest", "You have the best chance of having a problem-free pregnancy and a healthy baby if you follow a few simple guidelines:"]),
    ("• 9. Stop smoking \n• 10. Get some rest \n \nYou have the best chance of having a problem-free pregnancy and a healthy baby if you follow \na few simple guidelines:  \n\n1. Organise your pregnancy care early",
        ["• 9. Stop smoking", "• 10. Get some rest", "You have the best chance of having a problem-free pregnancy and a healthy baby if you follow a few simple guidelines:", "1. Organise your pregnancy care early"]),
    ("Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next. First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs. She took down a jar from one of the shelves as she passed; it was labelled 'ORANGE MARMALADE', but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody, so managed to put it into one of the cupboards as she fell past it.\n'Well!' thought Alice to herself, 'after such a fall as this, I shall think nothing of tumbling down stairs! How brave they'll all think me at home! Why, I wouldn't say anything about it, even if I fell off the top of the house!' (Which was very likely true.)",
        ["Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next.", "First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs.", "She took down a jar from one of the shelves as she passed; it was labelled 'ORANGE MARMALADE', but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody, so managed to put it into one of the cupboards as she fell past it.", "'Well!' thought Alice to herself, 'after such a fall as this, I shall think nothing of tumbling down stairs! How brave they'll all think me at home! Why, I wouldn't say anything about it, even if I fell off the top of the house!' (Which was very likely true.)"]),
    ("Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next. First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs. She took down a jar from one of the shelves as she passed; it was labelled 'ORANGE MARMALADE', but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody, so managed to put it into one of the cupboards as she fell past it.\r'Well!' thought Alice to herself, 'after such a fall as this, I shall think nothing of tumbling down stairs! How brave they'll all think me at home! Why, I wouldn't say anything about it, even if I fell off the top of the house!' (Which was very likely true.)",
        ["Either the well was very deep, or she fell very slowly, for she had plenty of time as she went down to look about her and to wonder what was going to happen next.", "First, she tried to look down and make out what she was coming to, but it was too dark to see anything; then she looked at the sides of the well, and noticed that they were filled with cupboards and book-shelves; here and there she saw maps and pictures hung upon pegs.", "She took down a jar from one of the shelves as she passed; it was labelled 'ORANGE MARMALADE', but to her great disappointment it was empty: she did not like to drop the jar for fear of killing somebody, so managed to put it into one of the cupboards as she fell past it.", "'Well!' thought Alice to herself, 'after such a fall as this, I shall think nothing of tumbling down stairs! How brave they'll all think me at home! Why, I wouldn't say anything about it, even if I fell off the top of the house!' (Which was very likely true.)"])
        ]

@pytest.mark.parametrize('text,expected_sents', PDF_TEST_DATA)
def test_en_pdf_type(text, expected_sents):
    """SBD tests from Pragmatic Segmenter for doctype:pdf"""
    seg = pysbd.Segmenter(language="en", clean=True, doc_type='pdf')
    segments = seg.segment(text)
    assert segments == expected_sents
