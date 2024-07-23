'''
V1.1
PROPERTY OF DAVID IBRAHIM
YOU MAY NOT EDIT, DISTRIBUTE, OR COPY
david@davidsamuel.me
'''


import sqlite3
import os
from datetime import datetime as dt

db = sqlite3.connect('inventory.db')
db.execute('PRAGMA journal_mode = MEMORY')
db.execute('CREATE TABLE IF NOT EXISTS items(item_code TEXT PRIMARY KEY, item_name TEXT DEFAULT NULL, item_price REAL DEFAULT 0, item_quantity INT DEFAULT 0)')
db.autocommit = True

if not os.path.exists('./receipts/'): os.mkdir('./receipts/')

screen = '0'
while True:
    os.system('cls')
    match screen:
        case '0':
            print('MAIN MENU\n')
            print(f'1. New receipt\n2. Edit inventory\n3. Check item\n')
            screen = input('Enter option number: ')
        
        case '1':
            print('NEW RECEIPT\n')
            items = []
            print('Scan items and Enter | Enter C to cancel\n')
            itemCode = input('\t')
            while itemCode != '' and itemCode.lower() != 'c':
                items.append(db.execute(f'SELECT * FROM items WHERE item_code = ?', (itemCode,)).fetchone())
                if items[-1] is not None: print(f'{len(items)}. {items[-1][1]}\t\t\t\t\t${items[-1][2]}')
                else: items.pop()
                itemCode = input('\t')
            if itemCode.lower() == 'c':
                screen = '0'
                continue
            total = sum([item[2] for item in items])
            print(f'Subtotal: ${total}')
            with open(f'./receipts/{dt.strftime(dt.now(), '%Y-%m-%d %H.%M.%S')}.csv', 'x') as receipt:
                receipt.write(f'CODE,NAME,PRICE\n')
                for item in items:
                    db.execute(f'UPDATE items SET item_quantity = item_quantity - 1 WHERE item_code = ?', (item[0],))
                    receipt.write(f'{item[0]},{item[1]},${item[2]}\n')
                receipt.write(f'Subtotal: ${total}')
            _=input()
            screen = '0'
        
        case '2':
            print('INVENTORY MENU\n')
            print(f'1. Add item\n2. Update item\n3. Remove item\n4. Export inventory\n5. Import inventory\n6. MAIN MENU\n')
            subscreen = input('Enter option number: ')
            match subscreen:
                case '1':
                    newItem = [input('Scan item to add | Enter C to cancel: ')]
                    if newItem[0].lower() == 'c' or \
                        db.execute('SELECT * FROM items WHERE item_code = ?', (newItem[0],)).fetchone() is not None: continue
                    newItem.append(input('Enter item name: '))
                    newItem.append(input('Enter item price: '))
                    newItem.append(input('Enter item quantity: '))
                    db.execute(f'''INSERT INTO items VALUES(?,?,?,?)''', (newItem[0], newItem[1], newItem[2] if newItem[2].isnumeric() else 0, newItem[3] if newItem[3].isnumeric() else 0))
                    print(f'Added {newItem[1]}')
                    _=input()
                
                case '2':
                    itemCode = input('Scan item to update | Enter C to cancel: ')
                    if itemCode.lower() == 'c': continue
                    item = db.execute(f'SELECT * FROM items WHERE item_code = ?', (itemCode,)).fetchone()
                    if item is not None:
                        print(f'1. Item name: {item[1]}\n2. Item price: ${item[2]}\n3. Item quantity: {item[3]}\n4. Cancel')
                        option = input('Enter option number to edit: ')
                        if option.lower() != '4': edit = input('Enter new value: ')
                        match option:
                            case '1':
                                db.execute(f'UPDATE items SET item_name = ? WHERE item_code = ?', (edit, item[0]))
                            case '2':
                                db.execute(f'UPDATE items SET item_price = ? WHERE item_code = ?', (edit, item[0]))
                            case '3':
                                db.execute(f'UPDATE items SET item_quantity = ? WHERE item_code = ?', (edit, item[0]))
                            case default:
                                continue
                        print(f'Updated {item[1]}')
                    else: print('Item not found...')
                    _=input()
                
                case '3':
                    itemCode = input('Scan item to remove | Enter C to cancel: ')
                    if itemCode.lower() == 'c': continue
                    db.execute(f'DELETE FROM items WHERE item_code = ?', (itemCode,))
                    print('Removed item if existed')
                    _=input()
                
                case '4':
                    items = db.execute('SELECT * FROM items ORDER BY item_name').fetchall()
                    with open(f'./inventory_export.csv', 'w') as file:
                        file.write(f'CODE,NAME,PRICE,QUANTITY\n')
                        for item in items:
                            file.write(f'{item[0]},{item[1]},${item[2]},{item[3]}\n')
                    print('Exported inventory to "inventory_export.csv"')
                    _=input()
                
                case '5':
                    if os.path.exists('./inventory_import.csv'):
                        with open(f'./inventory_import.csv') as file:
                            for item in file.readlines()[1:]:
                                item = item.split(',')
                                db.execute('INSERT OR REPLACE INTO items VALUES(?,?,?,?)', (item[0], item[1], item[2][1:], item[3]))
                        print('Imported inventory from "inventory_import.csv"')
                    else: print('"inventory_import.csv" not found...')
                    _=input()

                case '6':
                    screen = '0'
        
        case '3':
            print('CHECK ITEM\n')
            itemCode = input('Scan item to check | Enter C to cancel: ')
            if itemCode.lower() != 'c':
                item = db.execute(f'SELECT * FROM items WHERE item_code = ?', (itemCode,)).fetchone()
                if item is not None:
                    print(f'Item name: {item[1]}\nItem price: ${item[2]}\nItem quantity: {item[3]}')
                else: print('Item not found...')
                _=input()
            screen = '0'
        
        case default:
            screen = '0'



