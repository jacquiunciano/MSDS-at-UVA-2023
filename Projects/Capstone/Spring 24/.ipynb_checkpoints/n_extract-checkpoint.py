import fitz
import pandas as pd
import sys
from collections import Counter
import os
import glob

class Extraction():
    """

    """
    input_path = ""
    output_path = ""
    pdf_path = ""

    def __init__(self, input_path:"", output_path:"", pdf_path:""):
        self.input_path = input_path
        self.output_path = output_path
        self.pdf_path = pdf_path

    def flags_decomposer(flags):
    """Make font flags human readable."""
        l = []
        if flags & 2 ** 0:
            l.append("superscript")
        if flags & 2 ** 1:
            l.append("italic")
        if flags & 2 ** 2:
            l.append("serifed")
        else:
            l.append("sans")
        if flags & 2 ** 3:
            l.append("monospaced")
        else:
            l.append("proportional")
        if flags & 2 ** 4:
            l.append("bold")
        return ", ".join(l)

    def get_narrative(self, pdf):
        doc = fitz.open(pdf)

        style_counts = []

        for page in doc:
            #, flags=11

            paths = page.get_drawings()  # get drawings on the page

            drawn_lines = []
            for p in paths:
                # print(p)
                for item in p["items"]:
                    # print(item[0])
                    if item[0] == "l":  # an actual line
                        # print(item[1], item[2])
                        p1, p2 = item[1], item[2]
                        if p1.y == p2.y:
                            drawn_lines.append((p1, p2))
                    elif item[0] == "re":  # a rectangle: check if height is small
                        # print(item[0])
                        # print(item[1])
                        r = item[1]
                        if r.width > r.height and r.height <= 2:
                            drawn_lines.append((r.tl, r.tr))  # take top left / right points

            blocks = page.get_text("dict", flags=11)["blocks"]

            for b in blocks:  # iterate through the text blocks
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans

                        font_properties = "Font: '%s' (%s), size %g, color #%06x" % (
                            s["font"],  # font name
                            self.flags_decomposer(s["flags"]),  # readable font flags
                            s["size"],  # font size
                            s["color"],  # font color
                        )

                        r = fitz.Rect(s['bbox'])
                        for p1, p2 in drawn_lines:  # check distances for start / end points
                            if abs(r.bl - p1) <= 4 and abs(r.br - p2) <= 4:
                                font_properties = " ".join([font_properties, 'underlined'])

                        style_counts.append(font_properties)

        styles = dict(Counter(style_counts))

        style_list = sorted(styles.items(), key=lambda x:x[1], reverse=True)

        headers = {}
        count = 0
        p_size = int(style_list[0][0].split('size')[1].split()[0].strip(','))

        for page in doc:
            #, flags=11
            blocks = page.get_text("dict", flags=11)["blocks"]

            for b in blocks:  # iterate through the text blocks
                for l in b["lines"]:  # iterate through the text lines
                    texts = ""
                    count+=1
                    for s in l['spans']:
                        if s['size'] >= p_size:
                            texts = "".join ([texts, s['text']])
                    text_list = texts.split()
                    if len(text_list) > 0 and len(text_list) < 7:
                        headers.update({texts:count})

        opinion_loc = headers['Opinion']

        count = 0
        p_size = int(style_list[0][0].split('size')[1].split()[0].strip(','))
        new_headers = {}
        header_properties = ""

        for page in doc:
            #, flags=11
            blocks = page.get_text("dict", flags=11)["blocks"]

            for b in blocks:  # iterate through the text blocks
                for l in b["lines"]:  # iterate through the text lines
                    count+=1
                    if count==opinion_loc:
                        for s in l['spans']:
                            header_properties = "Font: '%s' (%s), size %g, color #%06x" % (
                                s["font"],  # font name
                                self.flags_decomposer(s["flags"]),  # readable font flags
                                s["size"],  # font size
                                s["color"],  # font color
                            )

        count = 0
        for page in doc:
            #, flags=11
            blocks = page.get_text("dict", flags=11)["blocks"]

            for b in blocks:  # iterate through the text blocks
                for l in b["lines"]:  # iterate through the text lines
                    count+=1
                    for s in l['spans']:
                        font_properties = "Font: '%s' (%s), size %g, color #%06x" % (
                            s["font"],  # font name
                            self.flags_decomposer(s["flags"]),  # readable font flags
                            s["size"],  # font size
                            s["color"],  # font color
                        )
                        if font_properties==header_properties:
                            new_headers.update({s['text']:count})

        p_size = int(style_list[0][0].split('size')[1].split()[0].strip(','))
        p_color = style_list[0][0].split('color')[1].split()[0].strip(',')
        p_font = style_list[0][0]

        bad_fonts = []

        for style in style_list:
            font_str = style[0]
            s_size = int(font_str.split('size')[1].split()[0].strip(','))
            s_color = font_str.split('color')[1].split()[0].strip(',')

            # if font matches paragraph font, it's a bad_font
            if font_str==p_font:
                bad_fonts+=[font_str]
            # if font doesn't match paragraph text color, it's a bad_font
            if s_color!=p_color:
                bad_fonts+=[font_str]
            # if font matches characteristics of vocab word font, it's a bad font
            if ('bold' in font_str and 'underlined' in font_str) and ('italic' in font_str and p_size==s_size):
                bad_fonts+=[font_str]
            # if font size is smaller than paragraph text size, it's a bad_font
            if s_size<p_size:
                bad_fonts+=[font_str]

        master = []
        for style in style_list:
            if style[0] not in bad_fonts:
                master += [style[0]]

        for page in doc:

            paths = page.get_drawings()  # get drawings on the page

            drawn_lines = []
            for p in paths:
                # print(p)
                for item in p["items"]:
                    # print(item[0])
                    if item[0] == "l":  # an actual line
                        # print(item[1], item[2])
                        p1, p2 = item[1], item[2]
                        if p1.y == p2.y:
                            drawn_lines.append((p1, p2))
                    elif item[0] == "re":  # a rectangle: check if height is small
                        # print(item[0])
                        # print(item[1])
                        r = item[1]
                        if r.width > r.height and r.height <= 2:
                            drawn_lines.append((r.tl, r.tr))  # take top left / right points

        count = 0
        opinion_subheaders = {}
        p_color = style_list[0][0].split('color')[1].split()[0].strip(',')

        for page in doc:
            #, flags=11
            blocks = page.get_text("dict", flags=11)["blocks"]

            for b in blocks:  # iterate through the text blocks
                for l in b["lines"]:  # iterate through the text lines
                    texts = ""
                    count+=1
                    span_fonts = []
                    if count>=opinion_loc:
                        for s in l['spans']:
                            font_properties = "Font: '%s' (%s), size %g, color #%06x" % (
                                s["font"],  # font name
                                self.flags_decomposer(s["flags"]),  # readable font flags
                                s["size"],  # font size
                                s["color"],  # font color
                            )

                            r = fitz.Rect(s['bbox'])
                            for p1, p2 in drawn_lines:  # check distances for start / end points
                                if abs(r.bl - p1) <= 4 and abs(r.br - p2) <= 4:
                                    font_properties = " ".join([font_properties, 'underlined'])

                            span_fonts+=[font_properties]
                            texts = "".join ([texts, s['text']])

                    text_list = texts.split()
                    if len(text_list) > 0 and len(text_list) < 7:
                        if any(i in span_fonts for i in master):
                            opinion_subheaders.update({texts:count})
                        if texts.isupper()==True:
                            opinion_subheaders.update({texts:count})

        narrative = ""
        conclusion_loc = 100000
        count = 0
        p_size = int(style_list[0][0].split('size')[1].split()[0].strip(','))

        keys_as_list = list(opinion_subheaders)
        for header_index in range(len(keys_as_list)):
            header = keys_as_list[header_index]
            if 'conclusion' in header.lower():
                conclusion_loc = opinion_subheaders[header]

        for page in doc:
            #, flags=11
            blocks = page.get_text("dict", flags=11)["blocks"]

            for b in blocks:  # iterate through the text blocks
                for l in b["lines"]:  # iterate through the text lines
                    texts = ""
                    count+=1
                    if count>=opinion_loc and count < conclusion_loc:
                        for s in l['spans']:
                            if s['size'] == p_size:
                                texts = "".join ([texts, s['text']])

                    narrative = " ".join([narrative, texts])


        return narrative.strip()

    def get_df(self):
        pdf_files = glob.glob("/*.pdf" % self.pdf_path)

        # Initialize DataFrame with corresponding row #
        df = pd.DataFrame(index=range(len(pdf_files)), columns=["CaseName", "Narrative"])

        for idx, file in enumerate(pdf_files):
            # Extract the title after the word "cases" in the file path
            if "50cases" in file:
                title = file.split("50cases/")[-1].split("/")[0]
            else:
                # Assuming the title is the filename without the extension
                title = os.path.splitext(os.path.basename(file))[0]

            narrative = self.get_narrative(file)

            # Replace the 'CaseName' and 'Narrative' in the DataFrame directly
            df.at[idx, "CaseName"] = title
            df.at[idx, "Narrative"] = narrative

    def save_narrative_to_txt(self, pdf_path, narrative):
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        txt_path = os.path.join(self.output_path, f"{base_name}.txt")

        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(narrative)

    def process_pdfs(self):
        pdf_files = glob.glob(os.path.join(self.input_folder, "*.pdf"))
        narratives = []

        for pdf_path in pdf_files:
            narrative = self.get_narrative(pdf_path)
            narratives.append(narrative)

            # Save narrative to text file in the same folder, overwriting existing files
            self.save_narrative_to_txt(pdf_path, narrative, output_folder, input_folder)