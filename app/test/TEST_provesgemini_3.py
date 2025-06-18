import sqlite3
import flet as ft
import os
from datetime import date

empresa = "TEST_Empresa_10"
BasedeDatos = f"bd_{empresa}.db"
ruta_BDapp = f"./test/{BasedeDatos}"


import sqlite3
import flet as ft

def mostrar_cuentas_expandibles_flet(ruta_BDapp: str, page: ft.Page) -> ft.Column:
    """
    Muestra de forma jerárquica los grupos, subgrupos y cuentas en un formato
    expandible/colapsable para Flet, con autoscroll.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
        page (ft.Page): La instancia de la página Flet para acceder a sus métodos.

    Returns:
        ft.Column: Un control Column que contiene todos los grupos expandibles y sus contenidos.
    """
    all_groups_controls = []
    conn = None
    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()

        # Obtener todos los grupos principales
        cursor.execute("SELECT grupo_id, descripcion_grupo FROM GRUPO ORDER BY grupo_id")
        grupos_principales = cursor.fetchall()

        if not grupos_principales:
            return ft.Column([ft.Text("No se encontraron grupos principales.", color=ft.Colors.RED_500, size=16)])

        for grupo_id, descripcion_grupo in grupos_principales:
            subgroup_tiles = [] # Lista para almacenar los ft.ExpansionTile de los subgrupos

            # Obtener subgrupos para el grupo actual
            cursor.execute("""
                SELECT
                    S.subgrupo_id,
                    S.cod_2,
                    S.descripcion_subgrupo
                FROM
                    SUBGRUPO S
                WHERE
                    S.grupo_id = ?
                ORDER BY
                    S.subgrupo_id
            """, (grupo_id,))
            subgrupos = cursor.fetchall()

            if not subgrupos:
                subgroup_tiles.append(
                    ft.Text(f"    No se encontraron subgrupos para el Grupo {str(grupo_id).zfill(2)}.",
                            size=14, color=ft.Colors.GREY_600)
                )

            for subgrupo_id, cod_subgrupo_completo, descripcion_subgrupo in subgrupos:
                account_texts = [] # Lista para almacenar los ft.Text de las cuentas

                # Obtener las cuentas de Nivel 3 para el subgrupo actual
                cursor.execute("""
                    SELECT
                        C.cod_3,
                        C.descripcion_n3
                    FROM
                        CUENTAS C
                    WHERE
                        C.grupo_id = ? AND C.subgrupo_id = ?
                    ORDER BY
                        C.nivel3_id
                """, (grupo_id, subgrupo_id))
                cuentas_nivel3 = cursor.fetchall()

                if not cuentas_nivel3:
                    account_texts.append(
                        ft.Text(f"        No hay cuentas para el subgrupo {cod_subgrupo_completo}.",
                                size=14, color=ft.Colors.GREY_500)
                    )

                for cod_full_n3, descripcion_n3 in cuentas_nivel3:
                    account_texts.append(
                        ft.Text(f"        {cod_full_n3} {descripcion_n3}",
                                size=14, color=ft.Colors.BLUE_GREY_500)
                    )

                # Crear un ExpansionTile para cada subgrupo
                subgroup_tiles.append(
                    ft.ExpansionTile(
                        title=ft.Text(f"{cod_subgrupo_completo} {descripcion_subgrupo}",
                                      size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700),
                        controls=account_texts,
                        #leading=ft.Icons(ft.Icons.FLOOD), # Opcional: un ícono
                        maintain_state=True # Mantiene el estado expandido/colapsado al redibujar
                    )
                )

            # Crear un ExpansionTile para cada grupo principal
            all_groups_controls.append(
                ft.ExpansionTile(
                    title=ft.Text(f"{str(grupo_id).zfill(2)} {descripcion_grupo}",
                                  size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                    controls=subgroup_tiles,
                    #leading=ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET), # Opcional: un ícono
                    maintain_state=True, # Mantiene el estado expandido/colapsado al redibujar
                    initially_expanded=False # Empieza colapsado
                )
            )
            all_groups_controls.append(ft.Divider()) # Separador entre grupos
            
        # Envolvemos todo en un ft.Column para contener los ExpansionTile
        # y lo metemos en un ft.ListView para el autoscroll
        return ft.Column(
            controls=all_groups_controls,
            scroll=ft.ScrollMode.ADAPTIVE, # Permite el autoscroll cuando el contenido excede el espacio
            expand=True # Permite que el Column se expanda para llenar el espacio disponible y habilitar el scroll
        )

    except sqlite3.Error as e:
        return ft.Column([ft.Text(f"Error de base de datos: {e}", color=ft.Colors.RED_500, size=16)])
    finally:
        if conn:
            conn.close()


def main(page: ft.Page):
    page.title = "Plan de Cuentas Expandible"
    page.vertical_alignment = ft.CrossAxisAlignment.START
    page.window_width = 400
    page.window_height = 700

    db_path = ruta_BDapp


    # Obtener el control Column que contiene los ExpansionTile y ya tiene el scroll
    content_column = mostrar_cuentas_expandibles_flet(db_path, page)

    page.add(content_column)
    page.update() # Es buena práctica llamar a update después de añadir o modificar controles

if __name__ == "__main__":
    ft.app(target=main)



