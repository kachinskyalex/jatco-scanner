import flet as ft
import cv2
from pyzbar.pyzbar import decode
import numpy as np

def main(page: ft.Page):
    page.title = "JATCO CVT QR"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"

    # Поля ввода - убрали всё лишнее
    extra_code = ft.TextField(label="Код (5 симв.)", width=250)
    disk_id = ft.TextField(label="ID (7 симв.)", width=250)
    
    result_display = ft.Text(value="Данные QR появятся здесь")

    def scan_qr(e):
        cap = cv2.VideoCapture(0) 
        if not cap.isOpened():
            print("Камера не найдена")
            return

        while True:
            ret, frame = cap.read()
            if not ret: break
            
            for obj in decode(frame):
                qr_data = obj.data.decode('utf-8')
                result_display.value = qr_data
                cap.release()
                cv2.destroyAllWindows()
                page.update()
                return

            cv2.imshow('QR Scanner (Press Q to exit)', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        page.update()

    def generate_csv(e):
        if not extra_code.value or not disk_id.value:
            return
        
        hex_prefix = disk_id.value.encode('utf-8').hex().upper()
        content = str(result_display.value)
        full_row = f"{hex_prefix},{content}"
        final_data = full_row[:100] if len(full_row) > 100 else full_row
        
        print(f"Результат: {final_data}")
        page.update()

    # Добавляем только базовые элементы
    page.add(
        ft.Text("JATCO QR Scanner", size=24),
        extra_code,
        disk_id,
        result_display,
        ft.ElevatedButton("ЗАПУСТИТЬ СКАНЕР", on_click=scan_qr),
        ft.ElevatedButton("СФОРМИРОВАТЬ ДАННЫЕ", on_click=generate_csv),
    )

ft.app(target=main)
