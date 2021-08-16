import json

"""
    Lista wszystkich wyszczególnionych wydziałów oraz grup (np. IT)
"""
DEPT_LIST = [{'short': ['SE', 'SK', 'ST', 'WS', 'BR'], 'long': 'Zarząd'},
             {'short': ['AI'], 'long': 'Wydział AI'},
             {'short': ['DR'], 'long': 'Wydział DR'},
             {'short': ['FN'], 'long': 'Wydział FN'},
             {'short': ['GN'], 'long': 'Wydział GN'},
             {'short': ['KM'], 'long': 'Wydział KM'},
             {'short': ['OR'], 'long': 'Wydział OR'},
             {'short': ['IT'], 'long': 'Informatycy'},
             {'short': ['OS'], 'long': 'Wydział OS'},
             {'short': ['OW'], 'long': 'Wydział OW'},
             {'short': ['SOP'], 'long': 'Wydział SOP'}]


def print_dept(dict, personnel):            # przyjmij dany wydział oraz listę wszystkich osób
    html_code = """    <div id=""" + """\"""" + dict['short'][0] + """\"""" + """ class="display">
            <h1><strong>""" + dict['long'] + """</strong></h1>
            <table data-name="mytable">
                <thead>
                    <tr class="header">
                        <th>Imię i nazwisko</th>
                        <th>Email</th>
                        <th>Telefon</th>
                        <th>Pokój</th>
                        <th>Budynek</th>
                    </tr>
                </thead>
                <tbody>
            """
    for n in personnel:
        print(n)
        member = [None]
        if n['userAccountControl'] == "514":            # zignoruj osoby z wyłączonym kontem
            continue
        if 'memberOf' in n:                             # sprawdź czy osoba posiada atrybut "memberOf" i przypisz
            member = n['memberOf']
        if n['dept'] in dict['short'] or member[0] in dict['short']:    # przypisz według wydziału lub grupy
            if member[0] == "Kierownicy":                               # osobna klasa oraz kolor tła dla kierowników
                html_code += """        <tr class="kier" style="background-color: #bbc2d0">
                        <td>""" + n['cn'] + """</td>
                        <td>""" + n['mail'] + """</td>
                        <td style="text-align:center">""" + "(67) 123-45-<b>" + n['telephoneNumber'] + """</b></td>
                        <td style="text-align:right">""" + str(int(n['physicalDeliveryOfficeName'][1::])) + """</td>
                        <td style="text-align:right">""" + n['physicalDeliveryOfficeName'][0] + """</td>
                    </tr>"""
            else:
                html_code += """
                    <tr>
                        <td>""" + n['cn'] + """</td>
                        <td>""" + n['mail'] + """</td>
                        <td style="text-align:center">""" + "(67) 123-45-<b>" + n['telephoneNumber'] + """</b></td>
                        <td style="text-align:right">""" + str(int(n['physicalDeliveryOfficeName'][1::])) + """</td>
                        <td style="text-align:right">""" + n['physicalDeliveryOfficeName'][0] + """</td>
                    </tr>"""
    html_code += """
                </tbody>
            </table>
        </div>"""
    return html_code


if __name__ == "__main__":
    with open("depts_list.json", 'r', encoding="utf-8") as open_list:         # otwórz listę wygenerowaną przez program
                                                                              # ldapextract2json.py
        personnel = json.load(open_list)

    html_code = """<html>
    <head>
        <script type="text/javascript" src="jquery/jquery-3.6.0.js"></script>
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
    <div id="whole">
    <div id="search"><input type="text" id="myInput" onkeyup="myFunction()" placeholder="Szukaj..."></div>
    """
    for each in DEPT_LIST:
        html_code += print_dept(each, personnel)
    html_code += """
    </div>
    <script>
        function check_fulls(table) {
	rows = table.getElementsByTagName("tr");
  var fulls = 0
  for (i=0; i<rows.length;i++) {
  	if (rows[i].style.display == "") {
    	fulls += 1
    }
  }
  return fulls
}


function myFunction() {
          var input, filter, table, tr, td, i,alltables;
            alltables = document.querySelectorAll("table[data-name=mytable]");
          input = document.getElementById("myInput");
          filter = input.value.toUpperCase();
          alltables.forEach(function(table){
              tr = table.getElementsByTagName("tr");
              for (i = 0; i < tr.length; i++) {
                td = tr[i].getElementsByTagName("td")[0];
                td1 = tr[i].getElementsByTagName("td")[2];
                td2 = tr[i].getElementsByTagName("td")[3];
                if (td) {
                  if (td.innerHTML.toUpperCase().indexOf(filter) > -1 | td1.innerHTML.indexOf(filter) > -1 | td2.innerHTML.indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    if (check_fulls(table) > 1){
                    	table.parentElement.style.display = ""
                      table.parentElement.style.marginBottom = "2.5em";
                    }
                  } else {
                    tr[i].style.display = "none";
                    if (check_fulls(table) == 1){
                    	table.parentElement.style.display = "none"
                      table.parentElement.style.marginBottom = "0";
                    }
                  }
                }       
              }
          });
        }
    </script>
    </body>
</html>"""
    with open("index.html", "w", encoding="utf-8") as html:
        html.write(html_code)
