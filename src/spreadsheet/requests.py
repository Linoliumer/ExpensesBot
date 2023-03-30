
async def add_sheets(service, data):
    title_cashless = f"{data['SET_ID']} CASHLESS"                # Shaping the sheet
    title_cash = f"{data['SET_ID']} CASH"
    # Create a new sheet of the current table
    result = service.spreadsheets().batchUpdate(
        spreadsheetId=data["SPREADSHEET_ID"],
        body=
        {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": title_cashless,
                            "gridProperties": {
                                "rowCount": 1000,
                                "columnCount": 20
                            }
                        }
                    }
                },
                {
                    "addSheet": {
                        "properties": {
                            "title": title_cash,
                            "gridProperties": {
                                "rowCount": 1000,
                                "columnCount": 20
                            }
                        }
                    }
                }
            ]
        }
    ).execute()
    data["CASHLESS_ID"] = result["replies"][0]["addSheet"]["properties"]["sheetId"]
    data["CASH_ID"] = result["replies"][1]["addSheet"]["properties"]["sheetId"]
    data["ID"] = result["replies"][0]["addSheet"]["properties"]["sheetId"]
    title = str(data["ID"])
    service.spreadsheets().batchUpdate(
        spreadsheetId=data["SPREADSHEET_ID"],
        body=
        {
            "requests": [
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": data["CASHLESS_ID"],
                            "dimension": "COLUMNS",
                            "startIndex": 0,
                            "endIndex": 7
                        },
                        "properties": {
                            "pixelSize": 200
                        },
                        "fields": "pixelSize"
                    }
                },
                {
                    "mergeCells": {
                        "range": {
                            "sheetId": data["CASHLESS_ID"],
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 6
                        },
                        "mergeType": "MERGE_ALL"
                    }
                },
                # Text Options
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": data["CASHLESS_ID"],
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 7
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "horizontalAlignment": 'CENTER',
                                "textFormat": {
                                    "bold": True,
                                    "fontSize": 12
                                }
                            }
                        },
                        "fields": "userEnteredFormat"
                    }
                },
                {
                    "repeatCell": {
                        "cell": {
                            "userEnteredFormat": {
                                "horizontalAlignment": 'CENTER',
                            }
                        },
                        "range": {
                            "sheetId": data["CASHLESS_ID"],
                            "startRowIndex": 1,
                            "endRowIndex": 2,
                            "startColumnIndex": 0,
                            "endColumnIndex": 7
                        },
                        "fields": "userEnteredFormat"
                    }
                },
                # Creating cell sides
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": data["CASHLESS_ID"],
                            "startRowIndex": 0,
                            "endRowIndex": 2,
                            "startColumnIndex": 0,
                            "endColumnIndex": 7
                        },
                        "right": {
                            "style": "SOLID",
                            "width": 1,
                            "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}
                        },
                        "bottom": {
                            "style": "SOLID",
                            "width": 1,
                            "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}
                        },
                        "innerHorizontal": {
                            "style": "SOLID",
                            "width": 1,
                            "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}
                        },
                        "innerVertical": {
                            "style": "SOLID",
                            "width": 1,
                            "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}
                        }
                    }
                },
                # LIST CASH
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": data["CASH_ID"],
                            "dimension": "COLUMNS",
                            "startIndex": 0,
                            "endIndex": 7
                        },
                        "properties": {
                            "pixelSize": 200
                        },
                        "fields": "pixelSize"
                    }
                },
                {
                    "mergeCells": {
                        "range": {
                            "sheetId": data["CASH_ID"],
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 6
                        },
                        "mergeType": "MERGE_ALL"
                    }
                },
                # Text Options
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": data["CASH_ID"],
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 7
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "horizontalAlignment": 'CENTER',
                                "textFormat": {
                                    "bold": True,
                                    "fontSize": 12
                                }
                            }
                        },
                        "fields": "userEnteredFormat"
                    }
                },
                {
                    "repeatCell": {
                        "cell": {
                            "userEnteredFormat": {
                                "horizontalAlignment": 'CENTER',
                            }
                        },
                        "range": {
                            "sheetId": data["CASH_ID"],
                            "startRowIndex": 1,
                            "endRowIndex": 2,
                            "startColumnIndex": 0,
                            "endColumnIndex": 7
                        },
                        "fields": "userEnteredFormat"
                    }
                },
                # Creating cell sides
                {
                    "updateBorders": {
                        "range": {
                            "sheetId": data["CASH_ID"],
                            "startRowIndex": 0,
                            "endRowIndex": 2,
                            "startColumnIndex": 0,
                            "endColumnIndex": 7
                        },
                        "right": {
                            "style": "SOLID",
                            "width": 1,
                            "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}
                        },
                        "bottom": {
                            "style": "SOLID",
                            "width": 1,
                            "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}
                        },
                        "innerHorizontal": {
                            "style": "SOLID",
                            "width": 1,
                            "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}
                        },
                        "innerVertical": {
                            "style": "SOLID",
                            "width": 1,
                            "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}
                        }
                    }
                },
            ]
        }
    ).execute()
    # Forming a request to fill in the cells
    service.spreadsheets().values().batchUpdate(spreadsheetId=data["SPREADSHEET_ID"], body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"{title_cash}!A1:G2",
             "majorDimension": "ROWS",
             "values": [
                 [f"Расходы Наличка", "", "", "", "", "", "Указатель"],
                 ["Дата", "Сумма", "Источник", "Категория", "Комментарий", "Пользователь",
                  "=ArrayFormula(ПОИСКПОЗ(1;ЕСЛИ(ЕПУСТО(A3:A);1;0);0))+2"]]
             },
            {"range": f"{title_cashless}!A1:G2",
             "majorDimension": "ROWS",
             "values": [
                 [f"Расходы Безналичка", "", "", "", "", "", "Указатель"],
                 ["Дата", "Сумма", "Источник", "Категория", "Комментарий", "Пользователь",
                  "=ArrayFormula(ПОИСКПОЗ(1;ЕСЛИ(ЕПУСТО(A3:A);1;0);0))+2"]]
             }
        ]
    }).execute()
    return data


async def add_entry_to_sheet(service, config, data):
    title = f"{config['SPREADSHEET']['SET_ID']} {data['type']}"
    pointer = int(
        service.
        spreadsheets().
        values().
        get(spreadsheetId=config["SPREADSHEET"]["SPREADSHEET_ID"], range=f"{title}!G2").execute()['values'][0][0]
    ) - 1
    # Query with entry
    service.spreadsheets().batchUpdate(
        spreadsheetId=config["SPREADSHEET"]["SPREADSHEET_ID"],
        body=
        {
            "requests": [
                {
                    "updateBorders": {
                        "range": {"sheetId": config["SPREADSHEET"][f"{data['type']}_ID"],
                                  "startRowIndex": pointer,
                                  "endRowIndex": pointer + 1,
                                  "startColumnIndex": 0,
                                  "endColumnIndex": 6
                                  },
                        "innerVertical": {
                            "style": "SOLID",
                            "width": 1,
                            "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}
                        },
                        "right": {
                            "style": "SOLID",
                            "width": 1,
                            "color": {"red": 0, "green": 0, "blue": 0, "alpha": 1}
                        }
                    }
                }
            ]
        }
    ).execute()
    if data["type"] == "CASHLESS":
        sources = data["sourcepayment"]
    else:
        sources = "Наличные"
    service.spreadsheets().values().batchUpdate(spreadsheetId=config["SPREADSHEET"]["SPREADSHEET_ID"], body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"{title}!A{pointer + 1}:F{pointer + 1}",
             "majorDimension": "ROWS",
             "values": [
                 [data["date"], data["amount"], sources,
                  data["category"], data["comment"], data["username"]]
             ]}
        ]
    }).execute()
