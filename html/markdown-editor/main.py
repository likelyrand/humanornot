# Flet App

import flet as ft
import markdown
import pyperclip
from html import escape


def main(page: ft.Page):

    page.title = "Human or Not Markdown Editor"
    page.theme_mode = "dark"

    def update_preview(e):
        # Updates the RHS(markdown/preview) when the content of the text field changes
        md.value = text_field.value
        page.update()

    def copy(e):
        to_copy = markdown.markdown(text_field.value).replace("\n", "<br />\n")
        to_copy = escape(to_copy)
        print("Copied to clipboard!")
        pyperclip.copy(to_copy)

    def clear(e):
        text_field.value = ""
        update_preview(e)
    
    text_field = ft.TextField(
        value="# Hello!\nYou can input text in the left text field and it will be shown on the right with appropriate markdown.\nYou can press \"Copy\" to copy the text in HTML format so you can paste it into Human or Not.\nSome examples: __bold text__, *italicized text*, ***all at once***",  # the initial value in the field (a simple Markdown code to test)
        multiline=True,
        expand=True,
        border_color=ft.Colors.TRANSPARENT,
        on_change=update_preview
    )
    md = ft.Markdown(
        value=text_field.value,
        selectable=True,
        extension_set="gitHubWeb",  
        on_tap_link=lambda e: page.launch_url(e.data),
    )
    
    page.add(
        ft.Row(
            controls=[
                text_field, 
                
                ft.VerticalDivider(color=ft.Colors.WHITE),
                
                ft.Container( 
                    ft.Column(  
                        [md],
                        scroll="hidden",
                    ),
                    expand=True,  
                    alignment=ft.alignment.top_left, 
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,  
        ) 
    )

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Text("Clear"),
                    margin=5,
                    padding=0,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.BLUE,
                    width=150,
                    height=30,
                    border_radius=5,
                    ink=True,
                    on_click=clear,
                ),
                ft.Container(
                    content=ft.Text("Copy"),
                    margin=5,
                    padding=0,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.BLUE,
                    width=150,
                    height=30,
                    border_radius=5,
                    ink=True,
                    on_click=copy,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    

ft.app(target=main)
