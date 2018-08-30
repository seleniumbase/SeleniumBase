title = '''<meta id="OGTitle" property="og:title" content="SeleniumBase">
        <title>Test Report</title>
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
            background-color: #c6d6f0;
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
            color: #0C8CDF;
            background-color: #c0f0ff;
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
        </style>'''

sh_style_test = (
    '''
    let test_tour = new Shepherd.Tour({
      defaults: {
        classes: 'shepherd-theme-dark',
        scrollTo: true
      }
    });
    ''')

sh_backdrop_style = (
    '''
    body.shepherd-active .shepherd-target.shepherd-enabled {
        box-shadow: 0 0 0 99999px rgba(0, 0, 0, 0.22);
        pointer-events:  none !important;
        z-index: 9999;
    }

    body.shepherd-active .shepherd-orphan {
        box-shadow: 0 0 0 99999px rgba(0, 0, 0, 0.16);
        pointer-events:  auto;
        z-index: 9999;
    }

    body.shepherd-active
        .shepherd-enabled.shepherd-element-attached-top {
            position: relative;
    }

    body.shepherd-active
        .shepherd-enabled.shepherd-element-attached-bottom {
            position: relative;
    }

    body.shepherd-active .shepherd-step {
        pointer-events:  auto;
        z-index: 9999;
    }

    body.shepherd-active {
        pointer-events:  none !important;
    }
    ''')
