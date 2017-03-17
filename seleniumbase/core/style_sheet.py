title = '''<meta id="OGTitle" property="og:title" content="SeleniumBase">
        <title>Selenium Base - Test Report</title>
        <link rel="SHORTCUT ICON"
        href="%s" /> ''' % (
            "https://raw.githubusercontent.com/seleniumbase/SeleniumBase"
            "/master/seleniumbase/resources/favicon.ico")

style = title + '''<style type="text/css">
        html {
            background-color: #9988ad;
        }
        html, body {
            font-size: 100%;
            box-sizing: border-box;
        }
        body {
            background-image: none;
            background-origin: padding-box;
            background-color: #fff;
            padding: 30;
            margin: 10;
            font-family: "Proxima Nova","proxima-nova",
            "Helvetica Neue",Helvetica,Arial,sans-serif !important;
            text-rendering: optimizelegibility;
            -moz-osx-font-smoothing: grayscale;
            box-shadow: 0px 2px 5px 1px rgba(0, 0, 0, 0.24),
            1px 2px 12px 0px rgba(0, 0, 0, 0.18) !important;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            box-shadow: 0px 2px 5px 1px rgba(0, 0, 0, 0.27),
            1px 2px 12px 0px rgba(0, 0, 0, 0.21) !important;
            transition: all 0.15s ease-out 0s;
            transition-property: all;
            transition-duration: 0.1s;
            transition-timing-function: ease-out;
            transition-delay: 0s;
        }
        table:hover {
            box-shadow: 0px 2px 5px 1px rgba(0, 0, 0, 0.35),
            1px 2px 12px 0px rgba(0, 0, 0, 0.28) !important;
        }
        thead th, thead td {
            padding: 0.5rem 0.625rem 0.625rem;
            font-weight: bold;
            text-align: left;
        }
        thead {
            text-align: center;
            border: 1px solid #e1e1e1;
            width: 150%;
            color: #fff;
            background-color: #999;
        }
        tbody tr:nth-child(even) {
            background-color: #f1f1f1;
        }
        tbody tr:nth-child(odd) {
            background-color: #ffffff;
        }
        tbody tr:nth-child(even):hover {
            background-color: #f8f8d2;
        }
        tbody tr:nth-child(odd):hover {
            background-color: #ffffe0;
        }
        tbody th, tbody td {
            padding: 0.5rem 0.625rem 0.625rem;
        }
        tbody {
            border: 1px solid #e1e1e1;
            background-color: #fefefe;
        }
        td {
            padding: 5px 5px 5px 0;
            vertical-align: top;
        }
        h1 table {
            font-size: 27px;
            text-align: left;
            padding: 0.5rem 0.625rem 0.625rem;
            font-weight: bold;
            padding-right: 10px;
            padding-left: 20px;
            padding: 15px 15px 15px 0;
        }
        h2 table {
            color: #0C8CDF;
            font-size: 16px;
            text-align: left;
            font-weight: bold;
            padding: 5px 5px 5px 0;
            padding-right: 10px;
            padding-left: 20px;
        }
        .summary{
            float: left;
            width: 100%;
            margin-bottom: 20px;
            box-shadow: 0px 2px 5px 1px rgba(0, 0, 0, 0.35), 1px 2px 12px 0px
                rgba(0, 0, 0, 0.28) !important;
        }
        .summary-report{
            width: 30%;
            margin-right: 5px;
            float:left;
            text-align: center;
            font-size: 20px;
            padding: 20px;
        }
        .summart-report-header{
            display: block
        }
        .header{
            float: left;
            width: 98.6%;
            margin: 0px;
            position: fixed;
            top: 0px;
            left: 9px;
            font-size: 32px;
            color: white;
            text-align: center;
            padding: 15px 0px;
            background: #20186f;
            font-weight: bold;
        }
        .log-result{
            background: #999;
            color: #FFF;
            border-bottom: 1px solid #fff;
        }
        .log-result-op{
            background: #fff;
            border-top: 1px solid #000;
        }
        .summart-report-passed{
            width: 30%;
            margin-right: 5px;
            float:left;
            text-align: center;
            font-size: 20px;
            padding: 20px;
            background:rgba(0, 128, 0, 0.5);
        }
        .summart-report-failed{
            width: 30%;
            margin-right: 5px;
            float:left;
            text-align: center;
            font-size: 20px;
            padding: 20px;
            background:rgba(255, 0, 0, 0.5);
            margin-right: 4px;
        }
        .summart-report-total{
            float:left;
            text-align: center;
            font-size: 20px;
            padding: 20px;
            background:rgba(128, 128, 128, 0.5);
            width: 31.5%;
            padding-right: 0px;
            margin-right: 0px;
        }
        </style>'''
