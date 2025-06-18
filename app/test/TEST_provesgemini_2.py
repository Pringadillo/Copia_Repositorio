import sqlite3
import flet as ft
import os
from datetime import date

empresa = "TEST_Empresa_10"
BasedeDatos = f"bd_{empresa}.db"
ruta_BDapp = f"./test/{BasedeDatos}"



def mostrar_cuentas_por_grupo_flet(ruta_BDapp: str, grupo_id_buscado: int) -> list[ft.Control]:
    """
    Muestra de forma jerárquica los subgrupos (Nivel 2) y cuentas (Nivel 3)
    para un grupo_id específico, formateado para Flet.

    Args:
        ruta_BDapp (str): La ruta al archivo de la base de datos SQLite.
        grupo_id_buscado (int): El ID del grupo a buscar.

    Returns:
        list[ft.Control]: Una lista de controles Flet (ft.Text) que representan
                          la jerarquía de subgrupos y cuentas.
    """
    formatted_controls = []
    conn = None
    try:
        conn = sqlite3.connect(ruta_BDapp)
        cursor = conn.cursor()

        # Opcional: Obtener la descripción del GRUPO principal para mostrarla al inicio
        cursor.execute("SELECT descripcion_grupo FROM GRUPO WHERE grupo_id = ?", (grupo_id_buscado,))
        grupo_data = cursor.fetchone()
        if grupo_data:
            formatted_controls.append(
                ft.Text(f"{str(grupo_id_buscado).zfill(2)} {grupo_data[0]}",
                        size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900)
            )
            formatted_controls.append(ft.Divider()) # Separador visual
        else:
            formatted_controls.append(ft.Text(f"No se encontró el Grupo ID: {grupo_id_buscado}",
                                            color=ft.Colors.RED_500, size=16))
            return formatted_controls # Si no hay grupo, salimos.

        # 1. Obtener todos los subgrupos (Nivel 2) para el grupo_id_buscado
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
        """, (grupo_id_buscado,))
        subgrupos = cursor.fetchall()

        if not subgrupos:
            formatted_controls.append(ft.Text(f"    No se encontraron subgrupos para el Grupo ID: {grupo_id_buscado}.",
                                            size=14, color=ft.colors.GREY_600))
            return formatted_controls

        # Iterar sobre cada subgrupo y luego buscar sus cuentas de nivel 3
        for subgrupo in subgrupos:
            subgrupo_id = subgrupo[0]
            cod_subgrupo_completo = subgrupo[1] # Esto es `cod_2` del subgrupo
            descripcion_subgrupo = subgrupo[2]

            # Formato para el título del subgrupo (Nivel 2)
            # Usamos cod_2 (ej. "1.01") para el prefijo si eso es lo que deseas mostrar
            # Si solo quieres el subgrupo_id dentro del grupo, usarías str(subgrupo_id).zfill(2)
            formatted_controls.append(
                ft.Text(f"  {cod_subgrupo_completo} {descripcion_subgrupo}",
                        size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700)
            )

            # 2. Obtener las cuentas de Nivel 3 para el subgrupo actual
            cursor.execute("""
                SELECT
                    C.nivel3_id,
                    C.descripcion_n3,
                    C.cod_3
                FROM
                    CUENTAS C
                WHERE
                    C.grupo_id = ? AND C.subgrupo_id = ?
                ORDER BY
                    C.nivel3_id
            """, (grupo_id_buscado, subgrupo_id))
            cuentas_nivel3 = cursor.fetchall()

            if not cuentas_nivel3:
                formatted_controls.append(ft.Text(f"        No hay cuentas para el subgrupo {cod_subgrupo_completo}.",
                                                size=14, color=ft.Colors.GREY_500))

            # 3. Añadir las cuentas de Nivel 3 con su formato
            for cuenta_n3 in cuentas_nivel3:
                nivel3_id = cuenta_n3[0] # No lo usamos en el formato actual, pero lo tenemos
                descripcion_n3 = cuenta_n3[1]
                cod_full_n3 = cuenta_n3[2] # Esto es `cod_3` de la cuenta

                # Formato para la cuenta (Nivel 3)
                # Usamos cod_3 (ej. "1.01.001") para el prefijo de la cuenta
                formatted_controls.append(
                    ft.Text(f"    {cod_full_n3} {descripcion_n3}",
                            size=14, color=ft.Colors.BLUE_GREY_500)
                )
        formatted_controls.append(ft.Divider()) # Separador visual al final de cada grupo
    except sqlite3.Error as e:
        formatted_controls.append(ft.Text(f"Error de base de datos: {e}",
                                        color=ft.Colors.RED_500, size=16))
    finally:
        if conn:
            conn.close()
    return formatted_controls

def main(page: ft.Page):
    page.title = "Contabilidad Doméstica"
    page.vertical_alignment = ft.MainAxisAlignment.START


    # Ejemplo de uso: Mostrar cuentas para GRUPO con grupo_id = 2 (Caixa Enginyers)
    grupo_id_a_mostrar = 2
    controles_cuentas = mostrar_cuentas_por_grupo_flet(ruta_BDapp, grupo_id_a_mostrar)

    # Una columna de Flet para contener la jerarquía de cuentas
    columna_cuentas = ft.Column(
        controls=controles_cuentas,
        spacing=0, # Reduce el espaciado entre líneas para una apariencia más compacta
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    page.add(
        ft.AppBar(title=ft.Text(f"Cuentas por Grupo: {grupo_id_a_mostrar}")),
        ft.Container(
            content=columna_cuentas,
            padding=20,
            alignment=ft.alignment.top_left,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)



