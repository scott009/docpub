#!/usr/bin/env python3
"""
Create What_is_RD_Thai.pdf from the bilingual chapter data
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json

# Paragraph data with Thai text
paragraphs = [
    {
        "id": "p9-1",
        "thai_id": "t9-1",
        "en": "Dharma is a Sanskrit word meaning \"truth,\" \"phenomena,\" or \"the nature of things.\" When it's capitalized, Dharma usually means the teachings of the Buddha and the practices based on those teachings.",
        "th": "ธรรมะเป็นคำภาษาสันสกฤตที่มีความหมายว่า \"ความจริง\" \"ปรากฏการณ์\" หรือ \"ธรรมชาติของสิ่งต่างๆ\" เมื่อเขียนด้วยตัวพิมพ์ใหญ่ ธรรมะมักหมายถึงคำสอนของพระพุทธเจ้าและการปฏิบัติที่มีรากฐานมาจากคำสอนเหล่านั้น"
    },
    {
        "id": "p9-2",
        "thai_id": "t9-2",
        "en": "The Buddha knew that all human beings, to some extent, strug gle with craving — the powerful, sometimes blinding desire to change our thoughts, feelings, or circumstances. Those of us who experience ad diction have been driven to use substances and/or harmful behaviors in a habitual pattern to try and create this desired change. Even though the Buddha didn't talk specifically about addiction, he understood the obsessive nature of the human mind. He understood our attachment to pleasure and aversion to pain. He understood the extreme measures we are willing to take, chasing what we want to feel and running away from feelings we fear. And he found a solution.",
        "th": "พระพุทธเจ้าทรงทราบว่ามนุษย์ทุกคนต่างต้องต่อสู้กับตัณหาในระดับหนึ่ง คือความปรารถนาอันทรงพลังและบางครั้งทำให้มองไม่เห็นสิ่งอื่น ที่ต้องการเปลี่ยนแปลงความคิด ความรู้สึก หรือสถานการณ์ของเรา พวกเราที่ประสบกับภาวะติดยาเสพติดถูกผลักดันให้ใช้สารเสพติด และ/หรือ พฤติกรรมที่เป็นอันตรายในรูปแบบที่เป็นนิสัยเพื่อพยายามสร้างการเปลี่ยนแปลงที่ปรารถนานี้ แม้ว่าพระพุทธเจ้าจะไม่ได้พูดถึงภาวะติดยาเสพติดโดยเฉพาะ แต่พระองค์เข้าใจธรรมชาติหมกมุ่นของจิตใจมนุษย์ พระองค์เข้าใจความยึดติดในความสุขและความเกลียดชังความทุกข์ พระองค์เข้าใจมาตรการที่รุนแรงที่เรายินดีทำ ไล่ตามสิ่งที่เราต้องการรู้สึกและหนีจากความรู้สึกที่เรากลัว และพระองค์พบทางออก"
    },
    {
        "id": "p9-3",
        "thai_id": "t9-3",
        "en": "This book describes a way to free ourselves from the suffering of addiction using Buddhist practices and principles. This program leads to recovery from addiction to substances like alcohol and drugs and from process addictions like sex, gambling, pornography, technology, work, codependence, shopping, eating, media, self-harm, lying, stealing, and obsessive worrying. This is a path to freedom from any repetitive and habitual behavior that causes suffering.",
        "th": "หนังสือเล่มนี้บรรยายถึงวิธีการปลดปล่อยตัวเราเองจากความทุกข์ของภาวะติดยาเสพติดโดยใช้การปฏิบัติและหลักการของพระพุทธศาสนา โปรแกรมนี้นำไปสู่การฟื้นฟูจากการติดสารเสพติดเช่นแอลกอฮอล์และยาเสพติด และจากการติดกระบวนการต่างๆ เช่น เพศสัมพันธ์ การพนัน ลามกอนาจาร เทคโนโลยี การทำงาน การพึ่งพาผู้อื่น การช็อปปิ้ง การกิน สื่อ การทำร้ายตนเอง การโกหก การขโมย และความกังวลเป็นทุนทรัพย์ นี่คือเส้นทางสู่เสรีภาพจากพฤติกรรมที่เกิดซ้ำและเป็นนิสัยที่ก่อให้เกิดความทุกข์"
    },
    {
        "id": "p9-4",
        "thai_id": "t9-4",
        "en": "Some of us reading this book may be unfamiliar with Buddhism or have not used Buddhist practices as a pathway to recovery. There might also be unfamiliar Buddhist words and concepts in this book. We also understand that what we present in this book does not encompass all Buddhist traditions, lineages, teachings, and practices, and may to some extent differ from your own Buddhist practice. Our aim is to clear ly describe our path and practice in Recovery Dharma for people new to recovery, new to Buddhism, and for those familiar with both. This book describes the original Buddhist teachings from which our program comes, the essence of Buddhism's fundamental and early teachings — the Four Noble Truths — to show how practicing the Eightfold Path is a pragmatic pathway which can transform the challenges of both early and long-term recovery.",
        "th": "พวกเราบางคนที่อ่านหนังสือเล่มนี้อาจไม่คุ้นเคยกับพระพุทธศาสนาหรือไม่เคยใช้การปฏิบัติของพระพุทธศาสนาเป็นเส้นทางสู่การฟื้นฟู อาจมีคำและแนวคิดของพระพุทธศาสนาที่ไม่คุ้นเคยในหนังสือเล่มนี้ เราเข้าใจด้วยว่าสิ่งที่เรานำเสนอในหนังสือเล่มนี้ไม่ครอบคลุมประเพณีพระพุทธศาสนาทั้งหมด สายวงศ์ คำสอน และการปฏิบัติ และอาจแตกต่างจากการปฏิบัติพระพุทธศาสนาของคุณในระดับหนึ่ง เป้าหมายของเราคือการอธิบายอย่างชัดเจนถึงเส้นทางและการปฏิบัติของเราในการฟื้นฟูด้วยธรรมะสำหรับผู้ที่เพิ่งเริ่มการฟื้นฟู เพิ่งเริ่มศึกษาพระพุทธศาสนา และสำหรับผู้ที่คุ้นเคยกับทั้งสองอย่าง หนังสือเล่มนี้อธิบายคำสอนดั้งเดิมของพระพุทธศาสนาที่โปรแกรมของเรามาจาก แก่นแท้ของคำสอนพื้นฐานและแรกเริ่มของพระพุทธศาสนา คือ อริยสัจสี่ เพื่อแสดงให้เห็นว่าการปฏิบัติตามมรรคมีองค์แปดคือเส้นทางที่เป็นจริงซึ่งสามารถเปลี่ยนแปลงความท้าทายของทั้งการฟื้นฟูในระยะแรกและระยะยาว"
    },
    {
        "id": "p9-5",
        "thai_id": "t9-5",
        "en": "This is a renunciation-based program. Regardless of our individ ual addictions, all of our members commit to a basic abstinence from that substance or behavior. For process addictions like food and technology, renunciation may mean establishing thoughtful boundaries and inten tions. For some of us, abstinence from things like obsessive sexual behav- ior, or compulsively seeking out love and relationships, may be necessary as we work to understand and find meaningful boundaries. Many of us have found that after renouncing our primary addiction for a period of time, other harmful behaviors and process addictions become apparent in our lives. Rather than getting discouraged, we found that we can meet these behaviors with compassion, wisdom, and patient investigation into our habitual tendencies. We believe recovery is a lifelong, holistic process of peeling back layers of habits and conditioned behaviors to find our own potential for awakening.",
        "th": "นี่คือโปรแกรมที่มีพื้นฐานจากการสละ โดยไม่คำนึงถึงความติดของเราแต่ละคน สมาชิกทุกคนของเราตั้งมั่นที่จะงดเว้นจากสารหรือพฤติกรรมนั้นโดยพื้นฐาน สำหรับการติดกระบวนการเช่นอาหารและเทคโนโลยี การสละอาจหมายถึงการตั้งขอบเขตและความตั้งใจที่รอบคอบ สำหรับพวกเราบางคน การงดเว้นจากสิ่งต่างๆ เช่น พฤติกรรมทางเพศที่หมกมุ่น หรือการแสวงหาความรักและความสัมพันธ์อย่างบีบบังคับ อาจจำเป็นในขณะที่เราทำงานเพื่อเข้าใจและหาขอบเขตที่มีความหมาย พวกเราหลายคนพบว่าหลังจากสละการติดหลักของเราไประยะหนึ่ง พฤติกรรมที่เป็นอันตรายอื่นๆ และการติดกระบวนการอื่นๆ ปรากฏชัดในชีวิตของเรา แทนที่จะท้อแท้ เราพบว่าเราสามารถพบพฤติกรรมเหล่านี้ด้วยความเมตตา ปัญญา และการสืบสวนอย่างอดทนในแนวโน้มนิสัยของเรา เราเชื่อว่าการฟื้นฟูเป็นกระบวนการแบบองค์รวมตลอดชีวิตของการลอกชั้นของนิสัยและพฤติกรรมที่มีเงื่อนไขเพื่อค้นหาศักยภาพของเราเองในการตื่นรู้"
    },
    {
        "id": "p9-6",
        "thai_id": "t9-6",
        "en": "Our program is peer-led: we do not follow any one teacher or leader. We support each other as partners walking the path of recovery together. This is not a program based in dogma or religion, but in find ing the truth for ourselves. This insight has worked for us, but is not the only path. It's fully compatible with other spiritual paths and programs of recovery. We know from our own experience that true recovery is only possible with the intention of radical honesty, understanding, awareness, and integrity, and we trust you to discover your own path.",
        "th": "โปรแกรมของเราเป็นแบบเพื่อนนำเพื่อน เราไม่ติดตามครูหรือผู้นำคนใดคนหนึ่ง เราสนับสนุนซึ่งกันและกันในฐานะคู่หูที่เดินบนเส้นทางการฟื้นฟูด้วยกัน นี่ไม่ใช่โปรแกรมที่มีพื้นฐานจากหลักคำสอนหรือศาสนา แต่อยู่บนการค้นหาความจริงด้วยตัวเราเอง ความเข้าใจนี้ได้ผลสำหรับเรา แต่ไม่ใช่เส้นทางเดียว มันเข้ากันได้อย่างสมบูรณ์กับเส้นทางจิตวิญญาณและโปรแกรมการฟื้นฟูอื่นๆ เราทราบจากประสบการณ์ของเราเองว่าการฟื้นฟูที่แท้จริงเป็นไปได้เท่านั้นด้วยความตั้งใจของความซื่อสัตย์อย่างสุดขั้ว ความเข้าใจ การตระหนักรู้ และความซื่อตรง และเราไว้วางใจให้คุณค้นพบเส้นทางของคุณเอง"
    },
    {
        "id": "p9-7",
        "thai_id": "t9-7",
        "en": "This is a program that asks us to never stop growing. It asks us to own our choices and be responsible for our own healing. It's based on mindfulness, kindness, generosity, forgiveness, and deep compassion.",
        "th": "นี่คือโปรแกรมที่ขอให้เราไม่หยุดเติบโต มันขอให้เราเป็นเจ้าของตัวเลือกของเราและรับผิดชอบต่อการรักษาของเราเอง มันมีพื้นฐานจากสติ ความกรุณา ความเอื้อเฟื้อเผื่อแผ่ การให้อภัย และความเมตตาอย่างลึกซึ้ง"
    },
    {
        "id": "p9-8",
        "thai_id": "t9-8",
        "en": "We do not rely on methods of shame and fear as motivators. These haven't worked in our own pasts, and have often created more struggle and suffering through relapse and discouragement. The courage it takes to recover from addiction is ultimately courage of the heart, and we aim to support each other as we commit to this brave work.",
        "th": "เราไม่พึ่งพาวิธีการของความอับอายและความกลัวเป็นแรงจูงใจ สิ่งเหล่านี้ไม่ได้ผลในอดีตของเรา และมักจะสร้างการต่อสู้และความทุกข์มากขึ้นผ่านการกลับไปเสพและความท้อแท้ ความกล้าหาญที่ต้องใช้ในการฟื้นฟูจากภาวะติดยาเสพติดคือความกล้าหาญของหัวใจในท้ายที่สุด และเรามุ่งหวังที่จะสนับสนุนซึ่งกันและกันในขณะที่เราตั้งมั่นกับงานที่กล้าหาญนี้"
    },
    {
        "id": "p9-9",
        "thai_id": "t9-9",
        "en": "Many of us have spent a lot of time criticizing ourselves. In this program, we renounce violence and doing harm, including the violence and harm we do to ourselves. We believe in the healing power of forgive ness. We put our trust in our own potential to awaken and recover, in the Four Noble Truths of the Buddha, and in the people we meet and connect with in meetings and throughout our journey in recovery.",
        "th": "พวกเราหลายคนใช้เวลามากในการวิพากษ์วิจารณ์ตนเอง ในโปรแกรมนี้ เราสละความรุนแรงและการทำอันตราย รวมถึงความรุนแรงและอันตรายที่เราทำกับตัวเราเอง เราเชื่อในพลังการรักษาของการให้อภัย เราวางความไว้วางใจในศักยภาพของเราเองที่จะตื่นรู้และฟื้นฟู ในอริยสัจสี่ของพระพุทธเจ้า และในผู้คนที่เราพบและเชื่อมต่อด้วยในการประชุมและตลอดการเดินทางของเราในการฟื้นฟู"
    },
    {
        "id": "p9-10",
        "thai_id": "t9-10",
        "en": "Of course we cannot escape the circumstances and conditions that are part of the human condition. We've already tried — through drugs and alcohol, through sex and codependency, through gambling and technology, through work and shopping, through food or the restric tion of food, through obsession and the futile attempts to control our experiences and feelings — and we're here because it didn't work. This is a program that invites us to recognize and accept that some pain and disappointment will always be present, to investigate the unskillful ways we have dealt with that pain in the past, and to develop a habit of under- standing, compassion, forgiveness, and insight toward our own pain, the pain of others, and the pain we have caused. Acceptance with insight and compassion is what creates freedom from the suffering that makes our pain seem unbearable.",
        "th": "แน่นอนว่าเราไม่สามารถหนีจากสถานการณ์และเงื่อนไขที่เป็นส่วนหนึ่งของสภาพความเป็นมนุษย์ เราได้ลองแล้ว ผ่านยาเสพติดและแอลกอฮอล์ ผ่านเพศสัมพันธ์และการพึ่งพาผู้อื่น ผ่านการพนันและเทคโนโลยี ผ่านการทำงานและการช็อปปิ้ง ผ่านอาหารหรือการจำกัดอาหาร ผ่านความหมกมุ่นและความพยายามที่ไร้ประโยชน์ในการควบคุมประสบการณ์และความรู้สึกของเรา และเราอยู่ที่นี่เพราะมันไม่ได้ผล นี่คือโปรแกรมที่เชิญเราให้รับรู้และยอมรับว่าความเจ็บปวดและความผิดหวังบางอย่างจะอยู่เสมอ เพื่อสืบสวนวิธีที่ไม่ชาญฉลาดที่เราจัดการกับความเจ็บปวดนั้นในอดีต และเพื่อพัฒนานิสัยของความเข้าใจ ความเมตตา การให้อภัย และความเข้าใจอย่างลึกซึ้งต่อความเจ็บปวดของเราเอง ความเจ็บปวดของผู้อื่น และความเจ็บปวดที่เราได้ทำให้เกิด การยอมรับพร้อมความเข้าใจอย่างลึกซึ้งและความเมตตาคือสิ่งที่สร้างเสรีภาพจากความทุกข์ที่ทำให้ความเจ็บปวดของเราดูเหมือนทนไม่ได้"
    },
    {
        "id": "p9-11",
        "thai_id": "t9-11",
        "en": "This book is only an introduction to a path that can bring lib eration and freedom from the cycle of addiction. The intention, and the hope of our program, is that every person on the path will be empowered to make it their own.",
        "th": "หนังสือเล่มนี้เป็นเพียงการแนะนำเส้นทางที่สามารถนำมาซึ่งการปลดปล่อยและเสรีภาพจากวงจรของภาวะติดยาเสพติด ความตั้งใจและความหวังของโปรแกรมของเราคือทุกคนบนเส้นทางจะได้รับพลังอำนาจให้ทำให้มันเป็นของตนเอง"
    },
    {
        "id": "p9-12",
        "thai_id": "t9-12",
        "en": "May you be happy.",
        "th": "ขอให้คุณมีความสุข"
    },
    {
        "id": "p9-13",
        "thai_id": "t9-13",
        "en": "May you be at ease.",
        "th": "ขอให้คุณสบายใจ"
    },
    {
        "id": "p9-14",
        "thai_id": "t9-14",
        "en": "May you be free from suffering.",
        "th": "ขอให้คุณปลอดจากความทุกข์"
    },
    {
        "id": "p9-15",
        "thai_id": "t9-15",
        "en": "May all beings be free from suffering.",
        "th": "ขอให้สัตว์ทั้งหลายปลอดจากความทุกข์"
    }
]

def create_pdf():
    # Create PDF
    output_file = "/mnt/c/Users/scott/Documents/AIProjects/Markdown/ThaiTranslation/What_is_RD_Thai.pdf"
    doc = SimpleDocTemplate(output_file, pagesize=letter,
                           leftMargin=0.75*inch, rightMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch,
                           title="Recovery Dharma - What is Recovery Dharma? (Thai)",
                           author="Recovery Dharma Global",
                           subject="Thai Translation of Recovery Dharma Chapter 9")

    # Register Thai font (using downloaded font file)
    import os

    thai_font_registered = False
    try:
        # First try the downloaded fonts
        script_dir = os.path.dirname(os.path.abspath(__file__))
        downloaded_fonts = [
            os.path.join(script_dir, 'fonts', 'Sarabun-Regular.ttf'),
            os.path.join(script_dir, 'fonts', 'NotoSansThai-Regular.ttf'),
        ]

        for downloaded_font in downloaded_fonts:
            if os.path.exists(downloaded_font):
                try:
                    pdfmetrics.registerFont(TTFont('ThaiFont', downloaded_font))
                    print(f"Registered Thai font: {downloaded_font}")
                    thai_font_registered = True
                    break
                except Exception as e:
                    print(f"Failed to register {downloaded_font}: {e}")
                    continue

        if not thai_font_registered:
            # Try common Thai font paths
            thai_font_paths = [
                '/usr/share/fonts/truetype/tlwg/Laksaman.ttf',
                '/usr/share/fonts/truetype/noto/NotoSansThai-Regular.ttf',
                '/usr/share/fonts/truetype/thai/Laksaman.ttf',
            ]

            for font_path in thai_font_paths:
                try:
                    if os.path.exists(font_path):
                        pdfmetrics.registerFont(TTFont('ThaiFont', font_path))
                        print(f"Registered Thai font: {font_path}")
                        thai_font_registered = True
                        break
                except Exception as e:
                    continue

        if not thai_font_registered:
            print("Warning: No Thai font found, Thai text may not display correctly")

    except Exception as e:
        print(f"Font registration error: {e}")

    # Define styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )

    title_thai_style = ParagraphStyle(
        'CustomTitleThai',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName='ThaiFont' if 'ThaiFont' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_CENTER,
        spaceAfter=6,
        textColor=colors.HexColor('#374151')
    )

    subtitle_thai_style = ParagraphStyle(
        'CustomSubtitleThai',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=colors.HexColor('#374151'),
        fontName='ThaiFont' if 'ThaiFont' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
    )

    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        spaceAfter=4,
        textColor=colors.HexColor('#dc2626'),
        fontName='Helvetica-Oblique'
    )

    disclaimer_thai_style = ParagraphStyle(
        'DisclaimerThai',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        spaceAfter=6,
        textColor=colors.HexColor('#dc2626'),
        fontName='ThaiFont' if 'ThaiFont' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
    )

    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )

    section_title_thai_style = ParagraphStyle(
        'SectionTitleThai',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='ThaiFont' if 'ThaiFont' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
    )

    para_id_style = ParagraphStyle(
        'ParaID',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#6b7280'),
        spaceAfter=4
    )

    para_style = ParagraphStyle(
        'ParaText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12,
        leading=14
    )

    para_thai_style = ParagraphStyle(
        'ParaTextThai',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12,
        leading=16,
        fontName='ThaiFont' if 'ThaiFont' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
    )

    # Build document content
    story = []

    # Title
    story.append(Paragraph("Recovery Dharma - รีคัฟเวอรีธรรมะ", title_style))

    # Subtitle
    story.append(Paragraph("How to Use Buddhist Practices and Principles to Heal the Suffering of Addiction", subtitle_style))
    story.append(Paragraph("วิธีใช้หลักธรรมะและการปฏิบัติแบบพุทธเพื่อเยียวยาความทุกข์จากการเสพติด", subtitle_thai_style))

    story.append(Spacer(1, 0.2*inch))

    # New disclaimer
    story.append(Paragraph("This Thai translation hasnt been reviewed by a human being. If you can help, please contact scott@farclass.com", disclaimer_style))
    story.append(Paragraph("การแปลภาษาไทยนี้ยังไม่ได้รับการตรวจสอบโดยมนุษย์ หากคุณสามารถช่วยได้ กรุณาติดต่อ scott@farclass.com", disclaimer_thai_style))

    # Blue horizontal line separator (closer to disclaimer)
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1e3a8a'), spaceAfter=0.2*inch, spaceBefore=0.05*inch))

    # Section title
    story.append(Paragraph("การฟื้นฟูด้วยธรรมะคืออะไร?", section_title_thai_style))
    story.append(Paragraph("WHAT IS RECOVERY DHARMA?", section_title_style))

    story.append(Spacer(1, 0.2*inch))

    # Paragraphs in table format
    for para in paragraphs:
        # Create table with two columns for bilingual text
        data = [
            [Paragraph(para['thai_id'], para_id_style), Paragraph(para['id'], para_id_style)],
            [Paragraph(para['th'], para_thai_style), Paragraph(para['en'], para_style)]
        ]

        t = Table(data, colWidths=[3.25*inch, 3.25*inch])
        t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        # Keep the paragraph ID and text together (prevent page breaks)
        story.append(KeepTogether([t, Spacer(1, 0.15*inch)]))

    # Build PDF
    doc.build(story)
    print(f"\nPDF created successfully: {output_file}")

if __name__ == "__main__":
    create_pdf()
