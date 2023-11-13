from bs4 import BeautifulSoup

html_code = '''<table class="table table-bordered fo_sz4">
                <tr class="active">
                    <td align="center">
                        <strong>SN</strong>
                    </td>
                    <td align="center">
                        <strong>Method of Use</strong>
                    </td>
                    <td align="center">
                        <strong>Crop</strong>
                    </td>
                    <td align="center">
                        <strong>Quantity per Acre</strong>
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <strong>1</strong>
                    </td>
                    <td>
                        Seed Treatment: Dissolve required quantity of bio fertilizer in 1.5 liter water
                        per acre and gently pour on the seeds. Turn the seeds up and down with the hand
                        till a uniform layer of bio fertilizer is formed on the seed. Keep the treated seed
                        in shade and sow immediately.
                    </td>
                    <td>
                        Wheat, Jowar, Maize, Cotton, Sun flower, Mustard
                    </td>
                    <td width="146">
                        2 kg 500 grams 200 grams
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <strong>2</strong>
                    </td>
                    <td>
                        Root Treatment: Prepare a solution in wide mouth bottle by dissolving required quantity
                        of bio fertilizer at the rate of 1 kg in 4 liter water. Soak the roots of the plants
                        for 3-4 minutes in this solution and then plant the treated roots immediately in
                        the field.
                    </td>
                    <td>
                        Paddy, Chili, Tomato, Cauliflower, Brinjal, Onion etc
                    </td>
                    <td>
                        1.5kg 2kg
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <strong>3</strong>
                    </td>
                    <td>
                        Tuber Treatment: Prepare a solution by dissolving required quantity of bio fertilizer
                        at the rate of 2 kg in 1.5 liter water. Soak the tuber of the plants for 5-10 minutes
                        in this solution or spray the solution on the tuber and then sow the treated tuber
                        immediately in the field.
                    </td>
                    <td>
                        For crops ripening within 6 months
                    </td>
                    <td>
                        2.5kg
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <strong>4</strong>
                    </td>
                    <td>
                        Soil Treatment: Prepare a mixture of required quantity of bio fertilizer with 35-40
                        kg compost or fine tilth and spray in the soil at the time of last plough or before
                        first irrigation.
                    </td>
                    <td>
                        For crops ripening in more than 6 months
                    </td>
                    <td>
                        3.5 kg
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <strong>5</strong>
                    </td>
                    <td colspan="3">
                        Blue Green Algae: Apply blue green algae at the rate of 12.5 kg per hectare after
                        one week of planting. At least 3-4 cm water must be filled in the field at the time
                        of its use. If any weed fungicides has been used, use blue green algae after 3-4
                        days of weed fungicides.
                    </td>
                </tr>
            </tbody></table>'''

# Parse the HTML code
soup = BeautifulSoup(html_code, 'html.parser')

# Find the table in the HTML
table = soup.find('table')

# Extract text content from the table
table_text = ""
if table:
    for row in table.find_all('tr'):
        row_text = ' | '.join(cell.get_text(strip=True).replace('\n','').replace('\t','') for cell in row.find_all(['td', 'th']))
        table_text += f"{row_text}\n"

# Print the resulting text
print(table_text)

# table_text='''SN | Fertilizer Name | Nitrogen | Phosphorus | Potash | Zinc
# 1 | Urea | 2.2 | - | - | -
# 2 | Calcium, Ammonium Nitrate | 4 | - | - | -
# 3 | Ammonium Sulphate | 5 | - | - | -
# 4 | Single Super Phosphate | - | 6.25 | - | -
# 5 | Murate of Potash | - | - | 1.7 | -
# 6 | Dy Ammonium Phosphate | 5.5 | 2.2 | - | -
# 7 | N.P.K. | 6.7 | 6.7 | 6.7 | -
# 8 | N.P.K. | 8.3 | 3.8 | 6.25 | -
# 9 | N.P. (Mixture) | 5 | 5 | - | -
# 10 | Rock Phosphate | - | 6 | - | -
# 11 | Zinc Sulphate | - | - | - | -
# 12 | Chilled Zinc | - | - | - | -'''
def table_to_json(table_text):
    # Split rows by newline character
    rows = table_text.strip().split('\n')

    # Split columns by " | " and create a list of dictionaries
    headers = [header.strip() for header in rows[0].split('|')]
    data = []
    for row in rows[1:]:
        values = [value.strip() for value in row.split('|')]
        row_dict = dict(zip(headers, values))
        data.append(row_dict)

    # Convert the list of dictionaries to JSON
    json_data = json.dumps(data, indent=2)
    return json_data

# import json
# result = table_to_json(table_text)
# print(result)