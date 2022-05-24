import pdfrw


def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict.keys():
                        if type(data_dict[key]) == bool:
                            if data_dict[key]:
                                annotation.update(pdfrw.PdfDict(
                                    AS=pdfrw.PdfName('Yes')))
                                # make annotation readonly
                                annotation.update(pdfrw.PdfDict(Ff=1))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            )
                            annotation.update(pdfrw.PdfDict(AP=''))
                            # make annotation readonly
                            annotation.update(pdfrw.PdfDict(Ff=1))

    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


def print_keys(template_pdf):
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    print(key)


def get_data_dict():
    company_name = "test_company"
    requested_by = "hanz zimmermann"

    data_dict = {
        'company_name': company_name,
        'requested_by': requested_by
    }
    return data_dict


if __name__ == '__main__':
    company_name = "Test_Company"
    pdf_template = "SamplePDF.pdf"
    pdf_output = "output.pdf"
    template_pdf = pdfrw.PdfReader(pdf_template)

    ANNOT_KEY = '/Annots'
    ANNOT_FIELD_KEY = '/T'
    ANNOT_VAL_KEY = '/V'
    ANNOT_RECT_KEY = '/Rect'
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'

    print_keys(template_pdf)
    # data with which to fill the pdf

    fill_pdf(pdf_template, pdf_output, data_dict=get_data_dict())
