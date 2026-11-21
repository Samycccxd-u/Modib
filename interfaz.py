import json
import math
import os
import random
import re
import shutil
import stat
import subprocess
import sys
import threading
import time
import tkinter as tk
import traceback
import zipfile
from pathlib import Path
from tkinter import filedialog, messagebox

# ---------- Colores (inspirados en balenaEtcher) ----------
FONDO = "#55595e"
AZUL = "#2297de"
AZUL_HOVER = "#3aa6ea"
GRIS_OFF = "#3b3e42"
GRIS_HECHO = "#46494e"
TEXTO_OFF = "#7b7f84"
BLANCO = "#ffffff"

ANCHO = 800
ALTO = 380
VERSION = "0.1.0"

# Icono de la ventana (PNG incrustado como texto: el icono del archivo .exe se pone al generarlo con --icon)
ICONO_PNG = "".join([
    "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAJ+ElEQVR42u2bbYxU1RnHf885987MzrCzb4qiQXBBoVmjaPG9",
    "poKmvlVjNaxpq7VpItHW0NpE+8EPSNJPmtjWWLHafrAlJi7RJrbxQ41gU6mhKFVbrba4iwiKCuwbOzN3557z9MOdWfdFYHfZ",
    "GRE8yWR3Zu69Z87/PK//5znCZ43VargPRUQB2h97f7mIXOd9fLGonorSDGo5ooY4hD4V6TEm2KSqz3avnLsBAFXhPoQ14ifc",
    "NeE5XWrpFAew8NH3b/bW3Cnqzpcwg7oy6mLwjiNyGIvYALEhWi6hYjcb5x/edvvcdePX9tkArN4YsGZZ3P7LN0+TXNOjks4u",
    "Jx7Gl4YAHIIk94gcmQioAoqigDWZHAQpNCps0KH+27t/0vG/6honAlBd/MNvX0Ym/5QJwjZXGIhFMCCGL+RQr4q32Xzg4/Je",
    "SgM3dd+5+IXRICQArOiyrO907Q+9vZxs/jlRn/blKBaRgKNgqGpswnSgYiIKA1d3r1q8obpmYbUa1qCnPPbe/BC7FZFmLUcO",
    "EcvRNFSdhGmLal8Zd86OlfO2sxox3AcoBOX4CUllmn05iuu1eCvJqz5OQqwvR7GkMs1BOX4CBe4Dg4hvX7v9JtvYdkmi87UX",
    "++qi+yJPb8mP+ay2GEjgCgOxbWy7pH3t9psQ8YYutSr+Hh9HKlJb624ErIGBYU8pVm5b0sSdX22m7JX+yGMluabGIIiPI1Xx",
    "99ClVhas7bkUazdqXFZqBIAA1giFsqfklGWnZLn7/BbOnZMB4PWPIx7YvI/newqEVsiFBucTX1YrqyhBKDi3zKj6GyTMAPha",
    "zBUYwSnsKTjmNYU8esUJdF0/h3PnZHAKTuGs2WnWXTuH3119IgtbQvYUHbEm99ZoeAkzqPobAkUuVhdTCXJmVM89sK/oOC5r",
    "WbW0lZVLmsiFBlWSSKUyo69s9TcX5rh8fpbfvt7P2n/28dGQozltMJIANYMiKepiFLlY2te+uw8TtMxUeGsqceJg5LFGuHHR",
    "LO46t4X5TSGQLORABm/0dzsHY36xpZeu/wxS9ko+nQDnZwoIY8HHvdK+9l03E5HeGD2Pla/NbeCe81u58OREz50HYzikmCng",
    "fWIsAbZ8WOKBzb1sfK9AJhCyM2of1Ev72u7DfpY1QuwSS356W8hdS1vo/ErjyK4app49qCYqVJWIp9/Zz4P/6OXtvcPk04aU",
    "FeIZEIfDAqBqo/pKntYGyw/OzHPH2c2JuFYWcbh2zGsiNSKwf9jzm9f6efy1fvYWHc0Zg3B49mFaAEglghuIFBH41umz+Ol5",
    "LSxoPrSeT3eMfmZPX5kHt/TyzDv78ark0xanmuSCtQSgqufF2FMoKxednOHu81u5ZG7DlPR82ho7zj68tLPIA5t72bSzSDYU",
    "GoKp24dJA1AVtYHIs6Al5MdLm/lORx4Z5cZMneJ6P86NPvnWIL/a0su23jL5tMEKkwZhUgBIJUpKW+Hmjjw/OqeZ5szM6flh",
    "2QdJfl9fyfPrrX2se3OAyCmGyYEwKfdnjdAfeVYtbeHei1ppzhhcxTgdaPHVYGf8azJiPtn7jHwqmc0Zw70XtbJqaUuSV0xy",
    "V6aU+WXDJKz1XgkPYeWmk1Uo07MfVqDsFGOEbDi1JwTTscR6iDmGnVIo6xgQVCETCJlADqpqxViJ4nH3ArlQCA+yq1XPNFWX",
    "OCUADoWt84o1wp+2DfGzFz+hJWNxPllMFCun5EOeueEkMoGM2e3q/wOR5/pnPmBPwRHaBDQr0B95HvnGCVx+avaQLnaqElQT",
    "8qMUK3sKDq8JKFU78vIHJZ7fXuDahbkx7sxXgHt2235e3V3iuAZLHOmIePdFnmFXm+S4JmyvEQhtIrKfviBjhXX/HphgI4wk",
    "tuXJNweZFSZubOy9UjMivmZ093gv4DzkUsLfdxV54+MII4kbcxVX9vKuIls/isiGMuLnp+I9jjgAxo9YwYpQjJU/vDkwAlJ1",
    "Y3//rwG8KkaSa+s1agpA1UfnQkPHcSmKsSefNjz37hAfFxzWJOrS01fmhfcK5FOGUqyccXyKtJWZy/0/TwlIQmXlljPypK0Q",
    "iLB7yPH0O4Mj1zz51iB9kUcEGlOGmzvylL3WpQBXcwBMJY294KQMF57cwMCwY1YoPPXWIE6T7/7430GaUoa+yHPpvCxnz04z",
    "VNa6hNh1sQFeEw9wS0eeslOyoeGNTyJe+bDEizuKbOstkw6SDOZ7Z+QxItNKbadF2tZjEmuEwWHPsnkNLGpLsWswJm0ND73S",
    "SzFWcqFh/7DnrBPSnDcnw9bd0UiMcFRIAMCwT2juFYsb2T+sNKUNL+0ssnV3icaUoVBWvl2h0WKtnxuoGwDV8LVzcSOzc5bI",
    "KSkrhDYhWObmA64/fVZdeYW6AlC16Cc3BlzZnmP/sMeIYEQYKivXnTaLtgZb3x9V57lGxi0deQKTsLrDTsmGwnc7Gj8XUqXu",
    "ADiFc05Ms3xew8hnV7XnWNSamhGa+4j0Ap81HrvqBPqjpBzZkrEVNZGjAwCRxOJbA4ogo2L+6t9caMiF5jNz+Sr7bI1gSJ5V",
    "K2xqAkAUK3uKSa0x9orXiQmOMirNk7FERuyVfUVHJkgA6K0hHzAlAHQSOw+wqC3FHWc3MSs0IwWL1oyZsMvj6Zvq29m5gNvO",
    "aiK0yWeFso4UV+Uwf+NhAVDl3A4Up5gKAheclOGCkzIHBelg381rCnnwsuMPmFsciH+YTkVqSgAUypo0Nlk56GRJGXssxzuV",
    "ipFWaLLRrKGRA9sBp4yw1IWyzjwAzieh60Ov9LKv6A5ZGEkY2ulbraoRnKgcE5OsKhs8ujDSlDYjXOQh5/qyNPZlcfTL8viX",
    "DRIzQXh8gVtkjvkmqWO7TS5QlR5jwxb1sZ8JSfCVUk5jyuBJyl1/6SmwcknThEZJM65R0kpSVxzfKNkQCG5G+1jViw2Nd67H",
    "CLpJbAAz3JpbDZlbGyylWPn5pn1c8dQunn5nP1Jpiq62yprK+z9vG+LKrp2sfmkvQ2WlrcEmZbWZzoMUFRsg6KZjvlla6FJ7",
    "6t7uLSadW6JRwQM1OyxRtQ8DkceK8P0z86SM8Ls3+oniJNxWqHVJzEk6a3w09FpPW/u5hk5xouZ+E6RFtbZ8dNIvAPmUIRMI",
    "j7/Wz8Ov9hEaSeJ3rfniUVU1QVpEzf10ihNUDaDtj7z7V5NrqtupEUb5eFcnKlBVY5vNB36o/2/dP1zwdaieGRKIw+BWHS71",
    "mTAdoFqXk5FVI1in1TsTpgMdLvXFYXArQuXM0BrxrFhvdqyc36OloRtVTCRh2qpqzFEyVDWWMG1VTKSloRt3rJzfw4r1hjXi",
    "E7+/vtOxemPQvWrxBkoD16iYvTabDxIQ1H+Bl+6rYq9i9lIauKZ71eINrN4YsL7TTWQajumjs9VxTB+eHpGEY+f4/P8BfkrD",
    "x2ppgCsAAAAASUVORK5CYII=",
])

N = 4              # pasos: launcher, carpeta, mod y organizar (el juego se elige antes)
COL = ANCHO // N   # ancho de cada paso

# Carpeta base: junto al .exe (si es un .exe) o junto a este archivo
if getattr(sys, "frozen", False):
    BASE = Path(sys.executable).parent
else:
    BASE = Path(__file__).resolve().parent

# Todo lo que Modib guarda junto al programa va en UNA sola carpeta: "Modib datos"
CARPETA_DATOS = BASE / "Modib datos"
# Aquí se recuerdan las carpetas que ya elegiste
ARCHIVO_CONFIG = CARPETA_DATOS / "config.json"

# Aquí se guardan un momento los mods que se descomprimen
CARPETA_TEMP = CARPETA_DATOS / "temporales"

# Subcarpeta del juego donde van los mods
CARPETA_MODS = "mods"
CARPETA_DESACTIVADOS = "mods_desactivados"  # donde van los mods apagados (juegos con mods en carpetas)

# Archivos que delatan la carpeta real de un mod
MARCADORES = ["_polymod_meta.json", "pack.json"]

# Juegos y cómo se instalan sus mods (edítalo cuando quieras)
# ---------- Dónde guarda cada launcher de Minecraft sus mods (Windows) ----------
def appdata():
    ruta = os.environ.get("APPDATA")
    return Path(ruta) if ruta else None


def hacer_unicas(lista):
    """Si dos entradas se llaman igual, añade el nombre de su carpeta para distinguirlas."""
    nombres = [e for e, _ in lista]
    resultado = []
    for etiqueta, ruta in lista:
        if nombres.count(etiqueta) > 1:
            carpeta = ruta.parent.name if ruta.name in ("minecraft", ".minecraft") else ruta.name
            etiqueta = f"{etiqueta} ({carpeta})"
        resultado.append((etiqueta, ruta))
    return resultado


def buscar_minecraft_fijo():
    """Minecraft Launcher, TLauncher y SKLauncher usan la carpeta .minecraft de AppData/Roaming."""
    base = appdata()
    ruta = base / ".minecraft" if base else None
    return [(".minecraft", ruta)] if ruta and ruta.is_dir() else []


def carpeta_instancias_prism():
    """Prism guarda sus instancias en AppData/Roaming/PrismLauncher/instances (o donde diga su config)."""
    base = appdata()
    if not base:
        return None
    datos = base / "PrismLauncher"
    try:
        for linea in (datos / "prismlauncher.cfg").read_text(encoding="utf-8", errors="ignore").splitlines():
            if linea.startswith("InstanceDir="):
                valor = linea.split("=", 1)[1].strip().strip('"')
                if valor:
                    ruta = Path(valor)
                    return ruta if ruta.is_absolute() else datos / ruta
    except OSError:
        pass
    return datos / "instances"


def nombre_instancia_prism(carpeta):
    try:
        for linea in (carpeta / "instance.cfg").read_text(encoding="utf-8", errors="ignore").splitlines():
            if linea.startswith("name="):
                nombre = linea.split("=", 1)[1].strip()
                if nombre:
                    return nombre
    except OSError:
        pass
    return carpeta.name


def buscar_prism():
    raiz = carpeta_instancias_prism()
    if not raiz or not raiz.is_dir():
        return []
    resultado = []
    for d in sorted(raiz.iterdir(), key=lambda p: p.name.lower()):
        if not d.is_dir() or d.name.startswith(("_", ".")) or not (d / "instance.cfg").exists():
            continue
        juego = next((d / n for n in ("minecraft", ".minecraft") if (d / n).is_dir()), d / "minecraft")
        resultado.append((nombre_instancia_prism(d), juego))
    return hacer_unicas(resultado)


def buscar_subcarpetas(raiz):
    """Cada subcarpeta de 'raiz' es un perfil/instancia con su propia carpeta mods."""
    if not raiz or not raiz.is_dir():
        return []
    return hacer_unicas([(d.name, d) for d in sorted(raiz.iterdir(), key=lambda p: p.name.lower())
                         if d.is_dir() and not d.name.startswith((".", "_"))])


def buscar_modrinth():
    base = appdata()
    return buscar_subcarpetas(base / "ModrinthApp" / "profiles" if base else None)


def buscar_curseforge():
    return buscar_subcarpetas(Path.home() / "curseforge" / "minecraft" / "Instances")


def buscar_feather():
    """Feather Client: busca carpetas 'mods' dentro de AppData/Roaming/.feather."""
    base = appdata()
    raiz = base / ".feather" if base else None
    if not raiz or not raiz.is_dir():
        return []
    ignorar = {"assets", "libraries", "runtime", "cache", "logs", "natives"}
    resultado = []
    for actual, carpetas, _ in os.walk(raiz):
        actual = Path(actual)
        if "mods" in carpetas:
            etiqueta = actual.relative_to(raiz).as_posix()
            resultado.append((".feather" if etiqueta == "." else etiqueta, actual))
            carpetas.remove("mods")
        carpetas[:] = [c for c in carpetas if c not in ignorar]
        if len(actual.relative_to(raiz).parts) >= 5:
            carpetas[:] = []
    return hacer_unicas(sorted(resultado, key=lambda x: x[0].lower()))


# ---------- Buscar un juego automáticamente por el PC ----------
IGNORAR_AL_BUSCAR = {"appdata", "node_modules", ".git", "windows", "$recycle.bin", "system volume information",
                     "__pycache__", "ddlc mods"}


def es_ddlc(carpeta):
    """El DDLC de verdad (no una copia con un mod, que Modib marca con modib_mod.json)."""
    return (carpeta / "DDLC.exe").is_file() and not (carpeta / "modib_mod.json").exists()


def es_fnf(carpeta):
    if any((carpeta / exe).is_file() for exe in ("Funkin.exe", "PsychEngine.exe")):
        return True
    nombre = carpeta.name.lower()
    return ("funkin" in nombre or nombre.startswith("fnf")) and \
           ((carpeta / "assets").is_dir() or (carpeta / "mods").is_dir())


def carpetas_steam(bases=None):
    """Carpetas 'steamapps/common' de todas las bibliotecas de Steam (donde Steam instala los juegos)."""
    if bases is None:
        bases = []
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as clave:
                bases.append(Path(winreg.QueryValueEx(clave, "SteamPath")[0]))
        except Exception:
            pass
        for letra in "CD":
            bases.append(Path(f"{letra}:/Program Files (x86)/Steam"))
    resultado = []
    for base in bases:
        resultado.append(base / "steamapps" / "common")
        try:
            texto = (base / "steamapps" / "libraryfolders.vdf").read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for ruta in re.findall(r'"path"\s+"([^"]+)"', texto):
            resultado.append(Path(ruta.replace("\\\\", "\\")) / "steamapps" / "common")
    return resultado


def raices_de_busqueda():
    """Sitios donde suele haber juegos: escritorio, documentos, descargas, carpetas de juegos y Steam."""
    casa = Path.home()
    raices = []
    for base in (casa, casa / "OneDrive"):
        for nombre in ("Desktop", "Escritorio", "Documents", "Documentos", "Downloads", "Descargas", "Games", "Juegos"):
            raices.append(base / nombre)
    for letra in "CDEF":
        for nombre in ("Games", "Juegos", "Steam", "SteamLibrary"):
            raices.append(Path(f"{letra}:/") / nombre)
    raices += carpetas_steam()
    vistas, unicas = set(), []
    for r in raices:
        if r.is_dir() and str(r).lower() not in vistas:
            vistas.add(str(r).lower())
            unicas.append(r)
    return unicas


def buscar_en_el_pc(reconocer, tiempo_max=12, profundidad=4, raices=None):
    """Recorre los sitios habituales y devuelve las carpetas que 'reconocer' acepta.
    Se detiene sola si tarda más de 'tiempo_max' segundos."""
    inicio = time.monotonic()
    encontrados, vistos = [], set()
    for raiz in (raices if raices is not None else raices_de_busqueda()):
        for actual, carpetas, _ in os.walk(raiz):
            if time.monotonic() - inicio > tiempo_max:
                return encontrados
            actual = Path(actual)
            if reconocer(actual):
                if str(actual).lower() not in vistos:
                    vistos.add(str(actual).lower())
                    encontrados.append(actual)
                carpetas[:] = []          # no hace falta mirar dentro del juego
                continue
            if len(actual.relative_to(raiz).parts) >= profundidad:
                carpetas[:] = []
            else:
                carpetas[:] = [c for c in carpetas if c.lower() not in IGNORAR_AL_BUSCAR]
    return encontrados


# tipo "fija": una sola carpeta conocida, se detecta sola.
# tipo "instancias": hay varias (una por instancia/perfil) y te deja elegir cuál.
# "descarga": True = ese launcher puede descargar mods él mismo (se lo recordamos al terminar).
# Para añadir otro launcher: una función que devuelva [(nombre, carpeta_del_juego), ...] y una línea aquí.
LAUNCHERS_MINECRAFT = {
    "Minecraft Launcher": {"tipo": "fija", "buscar": buscar_minecraft_fijo},
    "Prism Launcher": {"tipo": "instancias", "item": "instancia", "buscar": buscar_prism, "descarga": True},
    "TLauncher": {"tipo": "fija", "buscar": buscar_minecraft_fijo},
    "SKLauncher": {"tipo": "fija", "buscar": buscar_minecraft_fijo},
    "Modrinth App": {"tipo": "instancias", "item": "perfil", "buscar": buscar_modrinth, "descarga": True},
    "CurseForge": {"tipo": "instancias", "item": "instancia", "buscar": buscar_curseforge, "descarga": True},
    "Feather Client": {"tipo": "instancias", "item": "perfil", "buscar": buscar_feather},
}

#  - launchers: dónde puede estar el juego
#  - modo "carpeta":  el mod se copia como carpeta dentro de la carpeta "mods" del juego
#  - modo "fusionar": la carpeta "game" del mod se mezcla con la carpeta "game" del juego (guardando un respaldo)
#  - marcador: archivo que debe existir en la carpeta del juego (para no elegir la carpeta equivocada)
#  - reconocer: función que dice si una carpeta es la del juego (para el botón de buscar automáticamente)
#  - formato "jar": los mods son archivos .jar sueltos (como en Minecraft)
#  - info_launchers: juegos cuya carpeta se detecta sola según el launcher elegido
JUEGOS = {
    "Minecraft": {
        "launchers": list(LAUNCHERS_MINECRAFT),
        "modo": "carpeta",
        "formato": "jar",
        "info_launchers": LAUNCHERS_MINECRAFT,
    },
    "Friday Night Funkin'": {"corto": "FNF", "launchers": ["Juego suelto"], "modo": "carpeta",
                             "reconocer": es_fnf},
    "DDLC": {"launchers": ["Juego suelto", "Steam"], "modo": "fusionar", "marcador": "DDLC.exe",
             "reconocer": es_ddlc},
}


# ---------- Idiomas (español, inglés y portugués) ----------
IDIOMAS = {"es": "Español", "en": "English", "pt": "Português"}
idioma_actual = {"cod": "es"}

# Cada texto: (español, inglés, portugués). Entre llaves van los datos que se rellenan al mostrarlo.
TRADUCCIONES = {
    # --- pasos y botones ---
    "paso_launcher": ("Elegir launcher", "Choose launcher", "Escolher launcher"),
    "paso_carpeta": ("Elegir carpeta", "Choose folder", "Escolher pasta"),
    "paso_instancia": ("Elegir instancia", "Choose instance", "Escolher instância"),
    "paso_perfil": ("Elegir perfil", "Choose profile", "Escolher perfil"),
    "paso_mod": ("Elegir mod", "Choose mod", "Escolher mod"),
    "paso_organizar": ("¡Organizar!", "Organize!", "Organizar!"),
    "cambiar": ("Cambiar", "Change", "Alterar"),
    "btn_juegos": ("‹ Juegos", "‹ Games", "‹ Jogos"),
    "btn_mis_mods": ("Mis mods ›", "My mods ›", "Meus mods ›"),
    "btn_volver": ("‹ Volver", "‹ Back", "‹ Voltar"),
    "btn_abrir_carpeta": ("Abrir carpeta", "Open folder", "Abrir pasta"),
    "btn_actualizar": ("↻ Actualizar", "↻ Refresh", "↻ Atualizar"),
    "btn_idioma": ("Idioma: {nombre}", "Language: {nombre}", "Idioma: {nombre}"),
    "btn_acerca": ("Acerca de", "About", "Sobre"),
    "elegir": ("Elegir", "Choose", "Escolher"),
    "elige_juego": ("Elige el juego", "Choose a game", "Escolha o jogo"),
    "pie": ("Modib {version} · organiza tus mods sin líos",
            "Modib {version} · organize your mods hassle-free",
            "Modib {version} · organize seus mods sem complicação"),
    "juego_suelto": ("Juego suelto", "Standalone game", "Jogo avulso"),
    "descomprimido": ("(descomprimido)", "(extracted)", "(descompactado)"),
    "item_instancia": ("instancia", "instance", "instância"),
    "item_perfil": ("perfil", "profile", "perfil"),
    "item_carpeta": ("carpeta", "folder", "pasta"),
    "forge_antiguo": ("Forge (antiguo)", "Forge (old)", "Forge (antigo)"),
    "acerca": (
        "Modib {version}\nOrganiza los mods de tus juegos.\n\n"
        "Modib es un proyecto de la comunidad y no está afiliado a Mojang, Microsoft, Team Salvato, ni a los creadores de "
        "Friday Night Funkin' ni de ningún otro juego o launcher que aparezca aquí. Todos los nombres y marcas pertenecen a sus dueños.\n\n"
        "Descarga mods solo de sitios de confianza: un mod es un programa que se ejecuta en tu PC.",
        "Modib {version}\nOrganize the mods for your games.\n\n"
        "Modib is a community project and is not affiliated with Mojang, Microsoft, Team Salvato, the creators of "
        "Friday Night Funkin', or any other game or launcher shown here. All names and trademarks belong to their respective owners.\n\n"
        "Only download mods from sites you trust: a mod is a program that runs on your PC.",
        "Modib {version}\nOrganize os mods dos seus jogos.\n\n"
        "O Modib é um projeto da comunidade e não é afiliado à Mojang, à Microsoft, à Team Salvato, aos criadores de "
        "Friday Night Funkin' nem a nenhum outro jogo ou launcher citado aqui. Todos os nomes e marcas pertencem aos seus respectivos donos.\n\n"
        "Baixe mods apenas de sites confiáveis: um mod é um programa que roda no seu PC."),
    # --- errores generales ---
    "error_general": ("Algo salió mal:\n{error}", "Something went wrong:\n{error}", "Algo deu errado:\n{error}"),
    "error_log": ("Guardé los detalles en:\n{ruta}", "I saved the details in:\n{ruta}", "Salvei os detalhes em:\n{ruta}"),
    # --- tipos de mod de DDLC (lo que se ve bajo el nombre del mod) ---
    "tipo_desconocido": ("⚠ no reconozco su estructura", "⚠ structure not recognized", "⚠ estrutura não reconhecida"),
    "tipo_skins": ("solo skins", "skins only", "só skins"),
    "tipo_complemento": ("complemento de otro mod", "add-on for another mod", "complemento de outro mod"),
    "tipo_independiente": ("juego completo", "standalone game", "jogo completo"),
    "tipo_moderno": ("moderno (con su propio .exe)", "modern (has its own .exe)", "moderno (com .exe próprio)"),
    "tipo_clasico": ("clásico (va en game)", "classic (goes in game)", "clássico (vai em game)"),
    "popular": ("★ mod conocido: {nombre}", "★ well-known mod: {nombre}", "★ mod conhecido: {nombre}"),
    "no_reconozco_mod": (
        "No reconozco este mod: no trae una carpeta 'game' ni archivos que se puedan meter en ella.",
        "I don't recognize this mod: it has no 'game' folder and no files that can go into one.",
        "Não reconheço este mod: ele não tem uma pasta 'game' nem arquivos que possam ser colocados nela."),
    # --- carpeta del juego ---
    "launcher_sin_carpeta": (
        "No encontré la carpeta de {launcher} en AppData/Roaming.\nAbre el launcher una vez y vuelve a intentarlo, o pulsa el paso 2 para elegirla a mano.",
        "I couldn't find the {launcher} folder in AppData/Roaming.\nOpen the launcher once and try again, or click step 2 to choose it by hand.",
        "Não encontrei a pasta do {launcher} em AppData/Roaming.\nAbra o launcher uma vez e tente de novo, ou clique no passo 2 para escolher a pasta manualmente."),
    "donde_tienes_juego": ("¿Dónde tienes el juego?", "Where do you have the game?", "Onde está o jogo?"),
    "launcher_no_encontrado": (
        "No encontré {launcher} en el sitio habitual.\n¿Quieres elegir la carpeta a mano?",
        "I couldn't find {launcher} in the usual place.\nDo you want to choose the folder by hand?",
        "Não encontrei o {launcher} no local habitual.\nQuer escolher a pasta manualmente?"),
    "titulo_carpeta_launcher": (
        "Carpeta de {launcher} (la que contiene mods)",
        "{launcher} folder (the one that contains mods)",
        "Pasta do {launcher} (a que contém mods)"),
    "en_que_instalo": ("¿En qué {item} instalo el mod?", "Which {item} should I install the mod in?",
                       "Em qual {item} devo instalar o mod?"),
    "titulo_carpeta_juego": ("Carpeta de {juego}", "{juego} folder", "Pasta de {juego}"),
    "no_veo_marcador": (
        "No veo {marcador} en esa carpeta.\nElige la carpeta donde está {marcador} (la raíz del juego).",
        "I can't see {marcador} in that folder.\nChoose the folder where {marcador} is (the game's root folder).",
        "Não vejo {marcador} nessa pasta.\nEscolha a pasta onde está {marcador} (a raiz do jogo)."),
    "no_pude_buscar": ("No pude buscar:\n{error}", "I couldn't search:\n{error}", "Não consegui procurar:\n{error}"),
    "juego_no_encontrado": (
        "No encontré {juego} en los sitios habituales.\n¿Quieres elegir la carpeta a mano?",
        "I couldn't find {juego} in the usual places.\nDo you want to choose the folder by hand?",
        "Não encontrei {juego} nos locais habituais.\nQuer escolher a pasta manualmente?"),
    "encontre_varias": ("Encontré varias, ¿cuál es?", "I found several. Which one is it?", "Encontrei várias. Qual é?"),
    "buscando": ("Buscando el juego...", "Searching for the game...", "Procurando o jogo..."),
    "como_busco": ("¿Cómo busco la carpeta del juego?", "How should I look for the game folder?",
                   "Como devo procurar a pasta do jogo?"),
    "buscar_auto": ("Buscar automáticamente", "Search automatically", "Procurar automaticamente"),
    "elegir_mano": ("Elegir a mano", "Choose by hand", "Escolher manualmente"),
    # --- elegir el mod ---
    "elige_mod_jar": ("Elige tu mod de Minecraft (.jar)", "Choose your Minecraft mod (.jar)",
                      "Escolha seu mod de Minecraft (.jar)"),
    "tipo_jar": ("Mods de Minecraft", "Minecraft mods", "Mods de Minecraft"),
    "jar_invalido": ("Ese archivo no es un .jar válido o está dañado.", "That file is not a valid .jar or it is damaged.",
                     "Esse arquivo não é um .jar válido ou está danificado."),
    "como_es_mod": ("¿Cómo es tu mod?", "How is your mod packaged?", "Como é o seu mod?"),
    "archivo_zip": ("Archivo .zip", ".zip file", "Arquivo .zip"),
    "carpeta": ("Carpeta", "Folder", "Pasta"),
    "carpeta_del_mod": ("Carpeta de tu mod", "Your mod's folder", "Pasta do seu mod"),
    "elige_tu_mod": ("Elige tu mod", "Choose your mod", "Escolha seu mod"),
    "mods_comprimidos": ("Mods comprimidos", "Compressed mods", "Mods compactados"),
    "todos_archivos": ("Todos los archivos", "All files", "Todos os arquivos"),
    "solo_zip_o_carpeta": (
        "Por ahora solo puedo abrir mods en .zip, o carpetas ya descomprimidas.\nSi tu mod es un .rar o .7z, descomprímelo y elige la carpeta.",
        "For now I can only open mods in .zip format, or folders that are already extracted.\nIf your mod is a .rar or .7z, extract it and choose the folder.",
        "Por enquanto só consigo abrir mods em .zip ou pastas já descompactadas.\nSe o seu mod for .rar ou .7z, descompacte-o e escolha a pasta."),
    "zip_invalido": ("Ese archivo no es un .zip válido o está dañado.", "That file is not a valid .zip or it is damaged.",
                     "Esse arquivo não é um .zip válido ou está danificado."),
    "no_pude_descomprimir": ("No pude descomprimirlo:\n{error}", "I couldn't extract it:\n{error}",
                             "Não consegui descompactar:\n{error}"),
    "descomprimiendo": ("Descomprimiendo...", "Extracting...", "Descompactando..."),
    # --- organizar ---
    "organizando": ("Organizando...", "Organizing...", "Organizando..."),
    "instalando": ("Instalando...", "Installing...", "Instalando..."),
    "ya_instalado": ("'{mod}' ya está instalado en tu juego.", "'{mod}' is already installed in your game.",
                     "'{mod}' já está instalado no seu jogo."),
    "no_pude_instalar": (
        "No pude instalar el mod:\n{error}\n\nTu DDLC limpio no se tocó.",
        "I couldn't install the mod:\n{error}\n\nYour clean DDLC was not touched.",
        "Não consegui instalar o mod:\n{error}\n\nSeu DDLC limpo não foi alterado."),
    "confirmar_copia": (
        "Voy a crear una copia del juego para este mod (unos {mb} MB) en:\n{ruta}\n\nTu DDLC limpio no se toca. ¿Continuar?",
        "I'm going to create a copy of the game for this mod (about {mb} MB) in:\n{ruta}\n\nYour clean DDLC is not touched. Continue?",
        "Vou criar uma cópia do jogo para este mod (cerca de {mb} MB) em:\n{ruta}\n\nSeu DDLC limpo não é alterado. Continuar?"),
    "confirmar_complemento": (
        "'{mod}' se mezclará con la copia '{copia}', pisando los archivos que coincidan (no se guardan los originales).\nPara quitarlo habría que eliminar esa copia y volver a instalarla sin este complemento.\n\n¿Continuar?",
        "'{mod}' will be merged into the copy '{copia}', overwriting any files that match (the originals are not kept).\nTo remove it you would have to delete that copy and install it again without this add-on.\n\nContinue?",
        "'{mod}' será mesclado com a cópia '{copia}', substituindo os arquivos que coincidirem (os originais não são guardados).\nPara removê-lo seria preciso excluir essa cópia e instalá-la de novo sem este complemento.\n\nContinuar?"),
    "donde_lo_instalo": ("¿Dónde instalo '{mod}'?", "Where should I install '{mod}'?", "Onde devo instalar '{mod}'?"),
    "copia_nueva": ("Una copia nueva del juego limpio", "A new copy of the clean game", "Uma nova cópia do jogo limpo"),
    "aviso_steam": (
        "Esta parece la versión de Steam de DDLC. La mayoría de los mods dan errores con ella; lo recomendable es la versión gratuita de la web oficial.\n\n¿Continuar de todos modos?",
        "This looks like the Steam version of DDLC. Most mods give errors with it; the free version from the official website is recommended.\n\nContinue anyway?",
        "Esta parece ser a versão do Steam do DDLC. A maioria dos mods dá erro com ela; o recomendado é a versão gratuita do site oficial.\n\nContinuar mesmo assim?"),
    "aviso_antiguas": (
        "Tu DDLC tiene mods instalados con la versión anterior de Modib. Si sigues, la copia saldrá con esos cambios.\n\nLo mejor es deshacerlos antes desde «Mis mods».\n\n¿Continuar de todos modos?",
        "Your DDLC has mods installed by the previous version of Modib. If you continue, the copy will include those changes.\n\nIt's best to undo them first from \"My mods\".\n\nContinue anyway?",
        "Seu DDLC tem mods instalados pela versão anterior do Modib. Se continuar, a cópia sairá com essas alterações.\n\nO melhor é desfazê-los antes em \"Meus mods\".\n\nContinuar mesmo assim?"),
    "no_hay_espacio": (
        "No hay espacio suficiente en el disco: hacen falta unos {mb} MB y hay {libres} MB libres.",
        "There isn't enough disk space: about {mb} MB are needed and {libres} MB are free.",
        "Não há espaço suficiente no disco: são necessários cerca de {mb} MB e há {libres} MB livres."),
    "instalado_copia": (
        "¡Listo! '{mod}' está instalado en su propia copia del juego:\n{ruta}\n\nPulsa «Jugar» en «Mis mods» para abrirlo.",
        "Done! '{mod}' is installed in its own copy of the game:\n{ruta}\n\nClick \"Play\" in \"My mods\" to open it.",
        "Pronto! '{mod}' está instalado na própria cópia do jogo:\n{ruta}\n\nClique em \"Jogar\" em \"Meus mods\" para abri-lo."),
    "instalado_complemento": (
        "¡Listo! '{mod}' se añadió a la copia '{copia}'.",
        "Done! '{mod}' was added to the copy '{copia}'.",
        "Pronto! '{mod}' foi adicionado à cópia '{copia}'."),
    "consejo_errores": (
        "Si al abrirlo sale un error, prueba a borrar el archivo 'firstrun' de la carpeta 'game' de esa copia, o los datos guardados en %appdata%\\RenPy.",
        "If it shows an error when you open it, try deleting the 'firstrun' file in that copy's 'game' folder, or the saved data in %appdata%\\RenPy.",
        "Se der erro ao abrir, tente apagar o arquivo 'firstrun' da pasta 'game' dessa cópia, ou os dados salvos em %appdata%\\RenPy."),
    "btn_jugar": ("Jugar", "Play", "Jogar"),
    "btn_carpeta": ("Carpeta", "Folder", "Pasta"),
    "btn_eliminar": ("Eliminar", "Delete", "Excluir"),
    "btn_deshacer": ("Deshacer", "Undo", "Desfazer"),
    "confirmar_eliminar": (
        "¿Eliminar '{mod}'?\n\nSe borrará su carpeta de juego entera. Tu DDLC limpio no se toca. (Las partidas guardadas están en %appdata%\\RenPy y no se borran.)",
        "Delete '{mod}'?\n\nIts whole game folder will be deleted. Your clean DDLC is not touched. (Saved games are in %appdata%\\RenPy and are not deleted.)",
        "Excluir '{mod}'?\n\nA pasta inteira do jogo dele será apagada. Seu DDLC limpo não é alterado. (Os jogos salvos ficam em %appdata%\\RenPy e não são apagados.)"),
    "confirmar_deshacer": (
        "¿Deshacer '{mod}'?\n\nSe borrarán los archivos que añadió a tu DDLC y se devolverán los originales que pisó.",
        "Undo '{mod}'?\n\nThe files it added to your DDLC will be deleted and the original files it overwrote will be restored.",
        "Desfazer '{mod}'?\n\nOs arquivos que ele adicionou ao seu DDLC serão apagados e os originais que ele substituiu serão restaurados."),
    "no_pude_abrir": ("No pude abrir el juego:\n{error}", "I couldn't open the game:\n{error}", "Não consegui abrir o jogo:\n{error}"),
    "elige_ejecutable": ("¿Qué programa abro?", "Which program should I open?", "Qual programa devo abrir?"),
    "seccion_antiguas": (
        "Instalaciones de la versión anterior de Modib (dentro de tu DDLC)",
        "Installs from the previous version of Modib (inside your DDLC)",
        "Instalações da versão anterior do Modib (dentro do seu DDLC)"),
    "antiguo": ("(instalación antigua)", "(old install)", "(instalação antiga)"),
    "resumen_copias": ("{n} mods instalados", "{n} mods installed", "{n} mods instalados"),
    "es_copia": (
        "Esa carpeta es la copia de un mod, no el juego limpio. Elige tu DDLC limpio (donde está DDLC.exe).",
        "That folder is the copy of a mod, not the clean game. Choose your clean DDLC (where DDLC.exe is).",
        "Essa pasta é a cópia de um mod, não o jogo limpo. Escolha seu DDLC limpo (onde está o DDLC.exe)."),
    "no_es_copia": ("Esa carpeta no es una copia hecha por Modib.", "That folder is not a copy made by Modib.",
                    "Essa pasta não é uma cópia feita pelo Modib."),
    "ya_en_juego": (
        "'{mod}' ya está en tu juego. No lo copio para no pisarlo.",
        "'{mod}' is already in your game. I won't copy it so I don't overwrite it.",
        "'{mod}' já está no seu jogo. Não vou copiá-lo para não sobrescrevê-lo."),
    "como_prism": (" (como Prism)", " (like Prism)", " (como o Prism)"),
    "nota_descarga": (
        "Nota: ¡{launcher} puede descargar los mods por sí mismo{como}!",
        "Note: {launcher} can download mods by itself{como}!",
        "Nota: o {launcher} pode baixar os mods sozinho{como}!"),
    "no_pude_copiar": (
        "No pude copiar el mod:\n{error}\n\n¿Tienes el juego abierto?",
        "I couldn't copy the mod:\n{error}\n\nIs the game open?",
        "Não consegui copiar o mod:\n{error}\n\nO jogo está aberto?"),
    "listo_copiado": ("¡Listo! '{mod}' está en:\n{destino}", "Done! '{mod}' is in:\n{destino}",
                      "Pronto! '{mod}' está em:\n{destino}"),
    "es_mod_de": (
        "Es un mod de {loaders}. Tu perfil del launcher debe usar ese loader y la misma versión de Minecraft que el mod.",
        "This is a {loaders} mod. Your launcher profile must use that loader and the same Minecraft version as the mod.",
        "É um mod de {loaders}. Seu perfil no launcher deve usar esse loader e a mesma versão do Minecraft que o mod."),
    "loader_desconocido": (
        "No pude saber con qué loader funciona (Fabric, Forge...). Míralo en la página del mod.",
        "I couldn't tell which loader it works with (Fabric, Forge...). Check the mod's page.",
        "Não consegui saber com qual loader ele funciona (Fabric, Forge...). Confira na página do mod."),
    # --- lista de mods ---
    "mis_mods": ("Mis mods · {lugar}", "My mods · {lugar}", "Meus mods · {lugar}"),
    "ya_existe_destino": (
        "Ya existe '{nombre}' en el destino; no lo muevo para no pisarlo.",
        "'{nombre}' already exists at the destination; I won't move it so I don't overwrite it.",
        "'{nombre}' já existe no destino; não vou movê-lo para não sobrescrevê-lo."),
    "no_pude_cambiar": (
        "No pude cambiarlo:\n{error}\n\n¿Tienes el juego abierto?",
        "I couldn't change it:\n{error}\n\nIs the game open?",
        "Não consegui alterar:\n{error}\n\nO jogo está aberto?"),
    "resumen_mods": ("{activos} activos · {inactivos} desactivados", "{activos} enabled · {inactivos} disabled",
                     "{activos} ativos · {inactivos} desativados"),
    "sin_mods": ("Todavía no hay mods en esta carpeta.", "There are no mods in this folder yet.",
                 "Ainda não há mods nesta pasta."),
    "estado_activo": ("ACTIVO", "ENABLED", "ATIVO"),
    "estado_desactivado": ("DESACTIVADO", "DISABLED", "DESATIVADO"),
    "btn_activar": ("Activar", "Enable", "Ativar"),
    "btn_desactivar": ("Desactivar", "Disable", "Desativar"),
    "carpeta_esta_en": ("La carpeta está en:\n{ruta}", "The folder is at:\n{ruta}", "A pasta está em:\n{ruta}"),
}


def tr(clave, **datos):
    """El texto 'clave' en el idioma elegido (rellenando los {datos}). Si falta, usa español."""
    textos = TRADUCCIONES[clave]
    texto = textos[list(IDIOMAS).index(idioma_actual["cod"])]
    return texto.format(**datos) if datos else texto


def nombre_launcher(launcher):
    """'Juego suelto' se traduce; los nombres de launchers (Prism, TLauncher...) se dejan igual."""
    return tr("juego_suelto") if launcher == "Juego suelto" else launcher


def textos_pasos():
    return [tr("paso_launcher"), tr("paso_carpeta"), tr("paso_mod"), tr("paso_organizar")]

estado = {"juego": None, "launcher": None, "carpeta": None, "etiqueta": None, "mod": None}

# Estado del circulito de espera
espera = {"activo": False, "ocupado": False, "angulo": 0, "tarea": None}

ventana = tk.Tk()
ventana.title("Modib")
ventana.geometry(f"{ANCHO}x{ALTO}")
ventana.resizable(False, False)
ventana.configure(bg=FONDO)
try:
    ICONO = tk.PhotoImage(data=ICONO_PNG)   # se guarda en una variable para que Tk no lo pierda
    ventana.iconphoto(True, ICONO)
except tk.TclError:
    pass


def guardar_error(tipo, valor, tb):
    """Anota el error en 'Modib datos/errores.log' (para poder enviarlo si alguien pide ayuda). Devuelve la ruta."""
    try:
        archivo = CARPETA_DATOS / "errores.log"
        CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
        previo = archivo.read_text(encoding="utf-8", errors="ignore")[-100000:] if archivo.exists() else ""
        detalle = "".join(traceback.format_exception(tipo, valor, tb))
        archivo.write_text(previo + f"\n=== {time.strftime('%Y-%m-%d %H:%M:%S')} · Modib {VERSION} ===\n" + detalle,
                           encoding="utf-8")
        return archivo
    except OSError:
        return None


def mostrar_error(tipo, valor, tb):
    """Si algo falla por dentro, avisa en vez de quedarse mudo (útil en el .exe) y lo anota en un archivo."""
    mensaje = tr("error_general", error=valor)
    archivo = guardar_error(tipo, valor, tb)
    if archivo:
        mensaje += "\n\n" + tr("error_log", ruta=archivo)
    messagebox.showerror("Modib", mensaje)


ventana.report_callback_exception = mostrar_error


def crear_boton(padre, texto, comando):
    b = tk.Button(padre, text=texto, command=comando, font=("Segoe UI", 11),
                  bg=AZUL, fg=BLANCO, activebackground=AZUL_HOVER,
                  activeforeground=BLANCO, relief="flat", bd=0,
                  cursor="hand2", width=14, height=2,
                  disabledforeground=TEXTO_OFF)
    return b


def crear_boton_chico(padre, texto, comando, bg=GRIS_HECHO, ancho=12):
    return tk.Button(padre, text=texto, command=comando, font=("Segoe UI", 10),
                     bg=bg, fg=BLANCO, activebackground=AZUL_HOVER, activeforeground=BLANCO,
                     relief="flat", bd=0, cursor="hand2", width=ancho, height=1,
                     disabledforeground=TEXTO_OFF)


def elegir(titulo, opciones):
    """Ventanita con botones para elegir una opción."""
    resultado = []
    d = tk.Toplevel(ventana)
    d.title("Modib")
    d.configure(bg=FONDO)
    d.resizable(False, False)
    d.transient(ventana)
    d.grab_set()
    d.geometry(f"+{ventana.winfo_x() + 250}+{ventana.winfo_y() + 90}")
    tk.Label(d, text=titulo, bg=FONDO, fg=BLANCO,
             font=("Segoe UI", 12, "bold")).pack(padx=40, pady=(20, 10))
    for o in opciones:
        def pulsar(o=o):
            resultado.append(o)
            d.destroy()
        crear_boton(d, o, pulsar).pack(padx=40, pady=5, fill="x")
    tk.Label(d, text="", bg=FONDO).pack(pady=4)
    ventana.wait_window(d)
    return resultado[0] if resultado else None


def elegir_de_lista(titulo, opciones):
    """Como 'elegir', pero con una lista que se desplaza (para cuando hay muchas opciones)."""
    resultado = []
    d = tk.Toplevel(ventana)
    d.title("Modib")
    d.configure(bg=FONDO)
    d.resizable(False, False)
    d.transient(ventana)
    d.grab_set()
    d.geometry(f"+{ventana.winfo_x() + 250}+{ventana.winfo_y() + 40}")
    tk.Label(d, text=titulo, bg=FONDO, fg=BLANCO,
             font=("Segoe UI", 12, "bold")).pack(padx=40, pady=(20, 10))

    marco = tk.Frame(d, bg=FONDO)
    marco.pack(padx=40)
    barra = tk.Scrollbar(marco)
    lista = tk.Listbox(marco, height=10, width=min(max([34] + [len(o) + 2 for o in opciones]), 80), font=("Segoe UI", 11), bg=GRIS_OFF, fg=BLANCO,
                       selectbackground=AZUL, activestyle="none", relief="flat",
                       highlightthickness=0, yscrollcommand=barra.set)
    barra.config(command=lista.yview)
    for o in opciones:
        lista.insert("end", o)
    lista.pack(side="left")
    barra.pack(side="left", fill="y")

    def aceptar(evento=None):
        seleccion = lista.curselection()
        if seleccion:
            resultado.append(opciones[seleccion[0]])
            d.destroy()

    lista.bind("<Double-Button-1>", aceptar)
    crear_boton(d, tr("elegir"), aceptar).pack(padx=40, pady=14)
    ventana.wait_window(d)
    return resultado[0] if resultado else None


def elegir_flexible(titulo, opciones):
    """Botones si hay pocas opciones; lista con desplazamiento si hay muchas."""
    if len(opciones) <= 6:
        return elegir(titulo, opciones)
    return elegir_de_lista(titulo, opciones)


def migrar_archivos_viejos():
    """Las versiones anteriores dejaban modib_config.json y mods_descomprimidos sueltos junto al programa.
    Ahora van dentro de 'Modib datos': trae la configuración y quita la carpeta vieja si está vacía."""
    viejo = BASE / "modib_config.json"
    try:
        if viejo.is_file() and not ARCHIVO_CONFIG.exists():
            ARCHIVO_CONFIG.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(viejo), str(ARCHIVO_CONFIG))
        (BASE / "mods_descomprimidos").rmdir()      # solo se borra si está vacía
    except OSError:
        pass


# ---------- Recordar las carpetas que ya elegiste ----------
def cargar_config():
    try:
        datos = json.loads(ARCHIVO_CONFIG.read_text(encoding="utf-8"))
        return datos if isinstance(datos, dict) else {}
    except (OSError, ValueError):
        return {}


def guardar_config(datos):
    try:
        ARCHIVO_CONFIG.parent.mkdir(parents=True, exist_ok=True)
        ARCHIVO_CONFIG.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass   # si no se puede guardar, no pasa nada: solo habrá que volver a elegirlo


def recordar_carpeta():
    """Guarda la carpeta elegida para este juego y launcher, para no tener que elegirla otra vez."""
    if not (estado["juego"] and estado["launcher"] and estado["carpeta"]):
        return
    datos = cargar_config()
    datos[f"{estado['juego']}|{estado['launcher']}"] = {"carpeta": estado["carpeta"], "etiqueta": estado["etiqueta"]}
    guardar_config(datos)


def recuperar_carpeta():
    """Si ya habías elegido una carpeta para este juego y launcher (y sigue existiendo), la vuelve a usar."""
    guardado = cargar_config().get(f"{estado['juego']}|{estado['launcher']}")
    if isinstance(guardado, dict) and guardado.get("carpeta") and Path(guardado["carpeta"]).is_dir():
        estado.update(carpeta=guardado["carpeta"], etiqueta=guardado.get("etiqueta"))


def fijar_carpeta(ruta, etiqueta=None):
    estado.update(carpeta=str(ruta), etiqueta=etiqueta)
    recordar_carpeta()
    actualizar()


# ---------- Zips y carpetas temporales ----------
def limpiar_temporales():
    """Vacía la carpeta de temporales (restos de usos anteriores)."""
    if not CARPETA_TEMP.exists():
        return
    for elemento in CARPETA_TEMP.iterdir():
        if elemento.is_dir():
            shutil.rmtree(elemento, ignore_errors=True)
        else:
            try:
                elemento.unlink()
            except OSError:
                pass


def borrar_descomprimido(ruta_mod):
    """Borra de los temporales la copia de este mod (solo si está ahí)."""
    ruta_mod = Path(ruta_mod)
    if CARPETA_TEMP not in ruta_mod.parents:
        return  # el mod no venía de un zip: no tocamos nada
    carpeta_zip = CARPETA_TEMP / ruta_mod.relative_to(CARPETA_TEMP).parts[0]
    shutil.rmtree(carpeta_zip, ignore_errors=True)


def buscar_raiz_del_mod(carpeta):
    """Encuentra la carpeta que de verdad contiene el mod, aunque el zip tenga carpetas repetidas."""
    candidatos = []
    for marcador in MARCADORES:
        candidatos += list(carpeta.rglob(marcador))
    if candidatos:
        return min(candidatos, key=lambda p: len(p.parts)).parent

    # Sin marcador: si el zip trae una sola carpeta envoltorio, usamos esa
    def hijos(c):
        return [p for p in c.iterdir() if p.name != "__MACOSX"]

    contenido = hijos(carpeta)
    if len(contenido) == 1 and contenido[0].is_dir():
        carpeta = contenido[0]

    # ...y si dentro hay otra con el mismo nombre (carpeta repetida), bajamos también
    while True:
        contenido = hijos(carpeta)
        if (len(contenido) == 1 and contenido[0].is_dir()
                and contenido[0].name.lower() == carpeta.name.lower()):
            carpeta = contenido[0]
        else:
            return carpeta


def descomprimir(ruta_zip, modo="carpeta"):
    """Descomprime un zip en la carpeta de temporales. Devuelve la carpeta real del mod.
    (Si algo falla, lanza un error: lo muestra quien la llama.)"""
    destino = CARPETA_TEMP / ruta_zip.stem
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True)
    with zipfile.ZipFile(ruta_zip) as z:
        z.extractall(destino)
    if modo == "fusionar":
        return destino  # la raíz se busca al instalar
    return buscar_raiz_del_mod(destino)


def detectar_loaders(ruta_jar):
    """Mira dentro de un .jar para saber con qué loader funciona (Fabric, Forge...).
    Lanza zipfile.BadZipFile si el archivo no es un .jar válido."""
    pistas = {
        "fabric.mod.json": "Fabric",
        "quilt.mod.json": "Quilt",
        "META-INF/neoforge.mods.toml": "NeoForge",
        "META-INF/mods.toml": "Forge",
        "mcmod.info": tr("forge_antiguo"),
    }
    with zipfile.ZipFile(ruta_jar) as z:
        nombres = set(z.namelist())
    return [loader for archivo, loader in pistas.items() if archivo in nombres]


def copiar_mod(mod, destino, carpeta_mods):
    """Copia el mod a la carpeta del juego. Si falla a medias, limpia lo copiado."""
    carpeta_mods.mkdir(parents=True, exist_ok=True)
    try:
        if mod.is_dir():
            shutil.copytree(mod, destino)
        else:
            shutil.copy2(mod, destino)
    except Exception:
        if destino.is_dir():
            shutil.rmtree(destino, ignore_errors=True)
        raise
    borrar_descomprimido(mod)


def buscar_carpeta_game(carpeta):
    """Para mods que se mezclan con el juego (DDLC): encuentra la carpeta 'game' del mod.
    Si ya eligieron la propia carpeta 'game', se usa esa. Si hay varias, la más cercana a la raíz."""
    if carpeta.name.lower() == "game":
        return carpeta
    candidatos = [p for p in carpeta.rglob("*")
                  if p.is_dir() and p.name.lower() == "game" and "__MACOSX" not in p.parts]
    if not candidatos:
        return None
    return min(candidatos, key=lambda p: len(p.parts))


def revertir(carpeta_juego, respaldo, nuevos):
    """Deja el juego como estaba: borra lo que se añadió y devuelve los originales."""
    for rel in nuevos:
        try:
            (carpeta_juego / rel).unlink()
        except OSError:
            pass
    originales = respaldo / "originales"
    if originales.exists():
        for copia in originales.rglob("*"):
            if copia.is_file():
                destino = carpeta_juego / copia.relative_to(originales)
                destino.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(copia, destino)
    shutil.rmtree(respaldo, ignore_errors=True)
    try:
        respaldo.parent.rmdir()  # solo se borra si quedó vacía
    except OSError:
        pass


# Cómo reconoce Modib los distintos mods de DDLC
EXT_IMAGENES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
EXT_DEL_JUEGO = EXT_IMAGENES | {".rpa", ".rpyc", ".rpy", ".rpym", ".rpymc", ".ogg", ".mp3", ".wav", ".opus",
                                ".webm", ".ogv", ".mp4", ".ttf", ".otf"}
EXT_DOCUMENTOS = {".txt", ".md", ".pdf", ".url", ".html", ".htm", ".lnk", ".docx", ".rtf"}   # no se instalan
CARPETAS_DE_GAME = {"mod_assets", "submods", "images", "audio", "fonts", "gui", "python-packages", "cache",
                    "bgm", "sfx", "music", "scripts", "movies"}   # carpetas que ya van dentro de 'game'
CARPETAS_DE_LA_RAIZ = {"lib", "renpy", "characters"}               # carpetas que irían junto a DDLC.exe: no se copian


def raiz_sin_envoltorio(carpeta):
    """Si el zip trae una sola carpeta envoltorio (por ejemplo 'MiMod/'), entra en ella.
    No entra en carpetas que ya son parte de 'game' (como mod_assets o images)."""
    while True:
        hijos = [p for p in carpeta.iterdir() if p.name != "__MACOSX"]
        if len(hijos) == 1 and hijos[0].is_dir() and hijos[0].name.lower() not in CARPETAS_DE_GAME:
            carpeta = hijos[0]
        else:
            return carpeta


EXT_SKINS = EXT_IMAGENES | {".gift", ".sprite"}          # lo que lleva un mod de solo skins
EXT_PROGRAMAS = {".exe", ".dll", ".bat", ".cmd", ".sh", ".py", ".msi", ".ps1", ".vbs", ".app", ".jar"}   # no se copian en mods "sueltos"

# Mods muy conocidos: se reconocen por el nombre de su carpeta o zip, solo para mostrarlos bien
MODS_POPULARES = [
    ("monika after story", "Monika After Story"),
    ("blue skies", "Doki Doki Blue Skies"),
    ("salvation", "Doki Doki Salvation Remake"),
    ("exit music", "Doki Doki Exit Music"),
    ("purist", "Doki Doki Purist Mod"),
    ("world of dreams", "World of Dreams"),
    ("good ending", "The Good Ending"),
    ("rainclouds", "Doki Doki RainClouds"),
    ("rain clouds", "Doki Doki RainClouds"),
    ("fallen angel", "Doki Doki Fallen Angel"),
    ("relapse", "Doki Doki Relapse"),
    ("just natsuki", "Just Natsuki"),
    ("just yuri", "Just Yuri"),
    ("just sayori", "Just Sayori"),
]


def detectar_popular(nombre):
    """Si el nombre de la carpeta o del zip es el de un mod muy conocido, devuelve su nombre bonito."""
    limpio = re.sub(r"[_\-.]+", " ", nombre.lower())
    for clave, bonito in MODS_POPULARES:
        if clave in limpio:
            return bonito
    return None


def destino_en_ddlc(rel, modo):
    """Dónde va dentro de DDLC un archivo del mod ('rel' es su ruta dentro del mod)."""
    partes = rel.parts
    if len(partes) == 1 and rel.suffix.lower() == ".gift":                 # regalos de Monika After Story
        return Path("characters") / rel.name
    if partes[0].lower() == "gifts" and len(partes) > 1:
        return Path("characters").joinpath(*partes[1:])
    if partes[0].lower() in ("game", "lib", "renpy", "characters"):       # las carpetas del juego, siempre en minúsculas
        return Path(partes[0].lower()).joinpath(*partes[1:])
    if modo == "raiz":
        return rel
    return Path("game") / rel


def es_de_complemento(destino):
    """¿Este archivo es de los que se añaden a otro mod (submods, imágenes de mod_assets, regalos)?"""
    p = [x.lower() for x in destino.parts]
    if p[0] == "game" and len(p) > 2 and p[1] in ("submods", "mod_assets"):
        return True
    return p[0] == "characters" and destino.suffix.lower() == ".gift"


def clasificar_mod_fusion(mod):
    """Mira qué trae un mod de DDLC y cómo hay que instalarlo. Devuelve None si no lo reconoce.
      tipo "independiente": trae el juego entero (su .exe, game con audio/images/fonts, lib, renpy): no usa el DDLC base
      tipo "moderno":       trae game y lib/renpy o su propio .exe: se mezcla con una copia del DDLC limpio y se juega con su .exe
      tipo "clasico":       trae game sin más, o archivos sueltos (.rpa, .rpy, carpetas): va dentro de 'game' de una copia
      complemento:          True si solo trae skins, regalos o un submod: se añade a la copia de otro mod"""
    juego = buscar_carpeta_game(mod)
    if juego is None:
        origen, modo = raiz_sin_envoltorio(mod), "suelto"
    elif juego == mod:
        origen, modo = mod, "game"                            # eligieron la propia carpeta 'game'
    else:
        origen, modo = juego.parent, "raiz"
    tipo = "clasico"
    if modo == "raiz":
        hay_exe = any(f.is_file() and f.suffix.lower() == ".exe" for f in origen.iterdir())
        hay_motor = (origen / "lib").is_dir() or (origen / "renpy").is_dir()
        base_completa = all((juego / n).exists() for n in ("audio.rpa", "images.rpa", "fonts.rpa"))
        if hay_exe and hay_motor and base_completa:
            tipo = "independiente"
        elif hay_exe or hay_motor:
            tipo = "moderno"
    archivos, programas = [], set()
    for f in origen.rglob("*"):
        if not f.is_file() or "__MACOSX" in f.parts:
            continue
        rel = f.relative_to(origen)
        ext = f.suffix.lower()
        if tipo == "independiente":                           # un juego completo se copia tal cual
            archivos.append((f, rel))
            continue
        if len(rel.parts) == 1 and ext in EXT_DOCUMENTOS:
            continue                                           # un LEEME suelto no se instala
        if modo == "suelto" and ext in EXT_PROGRAMAS:
            programas.add(f.name)                              # en un mod suelto no se copian programas
            continue
        archivos.append((f, Path("game") / rel if modo == "game" else destino_en_ddlc(rel, modo)))
    if not archivos:
        return None
    solo_imagenes = tipo != "independiente" and all(d.suffix.lower() in EXT_SKINS for _, d in archivos)
    complemento = tipo != "independiente" and (solo_imagenes or all(es_de_complemento(d) for _, d in archivos))
    exes = sorted(d.name for _, d in archivos if len(d.parts) == 1 and d.suffix.lower() == ".exe")
    propios = [e for e in exes if e.lower() != "ddlc.exe"]
    return {"tipo": tipo, "origen": origen, "archivos": archivos, "ignoradas": sorted(programas),
            "solo_imagenes": solo_imagenes, "complemento": complemento,
            "ejecutables": propios or ["DDLC.exe"], "popular": detectar_popular(mod.name)}


clasificaciones = {}   # para no volver a mirar el mismo mod cada vez que se redibuja la ventana


def etiqueta_mod_fusion(ruta):
    """Texto corto que se muestra bajo el nombre del mod: qué tipo de mod es."""
    clave = str(ruta)
    if clave not in clasificaciones:
        try:
            clasificaciones[clave] = clasificar_mod_fusion(ruta)
        except OSError:
            clasificaciones[clave] = None
    info = clasificaciones[clave]
    if info is None:
        return tr("tipo_desconocido")
    if info["complemento"]:
        texto = tr("tipo_skins") if info["solo_imagenes"] else tr("tipo_complemento")
    else:
        texto = tr("tipo_" + info["tipo"])
    if info["popular"]:
        texto += "\n" + tr("popular", nombre=info["popular"])
    return texto


# ======================================================================
#  DDLC: cada mod en su propia copia del juego (como recomiendan las guías de la comunidad)
#    <carpeta del DDLC limpio>/../DDLC Mods/<Mod>/   copia del juego + el mod, con un modib_mod.json que la identifica
#  El DDLC limpio no se toca nunca.
# ======================================================================
NOMBRE_CARPETA_COPIAS = "DDLC Mods"
MARCA_COPIA = "modib_mod.json"


def carpeta_copias(carpeta_juego):
    return carpeta_juego.parent / NOMBRE_CARPETA_COPIAS


def tamano_carpeta(carpeta, ignorar=()):
    total = 0
    for actual, carpetas, archivos in os.walk(carpeta):
        carpetas[:] = [c for c in carpetas if c not in ignorar]
        for a in archivos:
            try:
                total += os.path.getsize(os.path.join(actual, a))
            except OSError:
                pass
    return total


def espacio_necesario(carpeta_juego, info):
    base = 0 if info["tipo"] == "independiente" else tamano_carpeta(carpeta_juego, ignorar=("modib_respaldo",))
    return base + sum(f.stat().st_size for f, _ in info["archivos"])


def comprobar_espacio(destino_padre, necesario):
    """Lanza OSError si no hay sitio en el disco para la copia."""
    existente = destino_padre
    while not existente.exists() and existente != existente.parent:
        existente = existente.parent
    libre = shutil.disk_usage(existente).free
    if libre < necesario * 1.05 + 50 * 1024 * 1024:
        raise OSError(tr("no_hay_espacio", mb=necesario // (1024 * 1024) + 1, libres=libre // (1024 * 1024)))


def listar_copias(carpeta_juego):
    """Las copias de mods que Modib ha creado: [{'nombre', 'ruta', 'tipo', 'ejecutables', 'popular', ...}]."""
    raiz = carpeta_copias(carpeta_juego)
    resultado = []
    if raiz.is_dir():
        for d in sorted((x for x in raiz.iterdir() if x.is_dir()), key=lambda x: x.name.lower()):
            datos = leer_json(d / MARCA_COPIA, dict)
            if datos:
                datos.update(nombre=d.name, ruta=d)
                resultado.append(datos)
    return resultado


def instalar_ddlc_copia(mod, carpeta_juego, info):
    """Crea la copia del juego para este mod y mete el mod dentro. El DDLC limpio no se toca."""
    destino = carpeta_copias(carpeta_juego) / mod.name
    if destino.exists():
        raise ValueError(tr("ya_instalado", mod=mod.name))
    comprobar_espacio(destino.parent, espacio_necesario(carpeta_juego, info))
    try:
        if info["tipo"] == "independiente":
            destino.mkdir(parents=True)                      # trae el juego entero: no hace falta el base
        else:
            shutil.copytree(carpeta_juego, destino, ignore=shutil.ignore_patterns("modib_respaldo", MARCA_COPIA))
        for origen, rel in info["archivos"]:
            d = destino / rel
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origen, d)
        escribir_json(destino / MARCA_COPIA, {
            "tipo": info["tipo"], "ejecutables": info["ejecutables"], "popular": info["popular"],
            "fecha": time.strftime("%Y-%m-%d %H:%M"), "complementos": []})
    except Exception:
        shutil.rmtree(destino, ignore_errors=True)
        try:
            destino.parent.rmdir()
        except OSError:
            pass
        raise
    borrar_descomprimido(mod)
    return {"destino": destino, "copia": None}


def instalar_complemento(mod, carpeta_juego, info, nombre_copia):
    """Añade skins, regalos o un submod a la copia de otro mod (se mezcla con lo que haya)."""
    copia = carpeta_copias(carpeta_juego) / nombre_copia
    datos = leer_json(copia / MARCA_COPIA, dict)
    if not datos:
        raise ValueError(tr("no_es_copia"))
    for origen, rel in info["archivos"]:
        d = copia / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origen, d)
    datos.setdefault("complementos", []).append(mod.name)
    escribir_json(copia / MARCA_COPIA, datos)
    borrar_descomprimido(mod)
    return {"destino": copia, "copia": nombre_copia}


def _forzar_borrado(funcion, ruta, _error):
    os.chmod(ruta, stat.S_IWRITE)                             # archivos de solo lectura
    funcion(ruta)


def eliminar_copia(carpeta_juego, nombre):
    """Borra la copia de un mod (solo si la hizo Modib; nunca toca el DDLC limpio)."""
    copia = carpeta_copias(carpeta_juego) / nombre
    if not (copia / MARCA_COPIA).is_file():
        raise ValueError(tr("no_es_copia"))
    shutil.rmtree(copia, onerror=_forzar_borrado)
    try:
        copia.parent.rmdir()                                  # si ya no quedan copias, se quita la carpeta
    except OSError:
        pass


# ======================================================================
#  Instalaciones de versiones anteriores de Modib (mezcladas dentro del DDLC limpio): solo se pueden deshacer
# ======================================================================
def carpeta_respaldo(carpeta_juego):
    return carpeta_juego / "modib_respaldo"


def leer_json(ruta, tipo):
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        return datos if isinstance(datos, tipo) else tipo()
    except (OSError, ValueError):
        return tipo()


def escribir_json(ruta, datos):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")


def leer_indice(carpeta_juego):
    return leer_json(carpeta_respaldo(carpeta_juego) / "_base" / "indice.json", dict)


def guardar_indice(carpeta_juego, indice):
    escribir_json(carpeta_respaldo(carpeta_juego) / "_base" / "indice.json", indice)


def leer_mods_instalados(carpeta_juego):
    """{nombre: info} de los mods instalados con este sistema (los que tienen info.json)."""
    resultado = {}
    raiz = carpeta_respaldo(carpeta_juego)
    if raiz.is_dir():
        for d in raiz.iterdir():
            if d.is_dir() and not d.name.startswith("_"):
                info = leer_json(d / "info.json", dict)
                if isinstance(info.get("archivos"), list) and isinstance(info.get("orden"), int):
                    resultado[d.name] = info
    return resultado


def listar_mods_ddlc(carpeta_juego):
    """[(nombre, activo, antiguo)] de lo que Modib instaló en DDLC. 'antiguo' = instalado con una versión
    anterior de Modib: esos solo se pueden desinstalar."""
    raiz = carpeta_respaldo(carpeta_juego)
    if not raiz.is_dir():
        return []
    nuevos = leer_mods_instalados(carpeta_juego)
    resultado = [(n, bool(i.get("activo")), False) for n, i in nuevos.items()]
    for d in raiz.iterdir():
        if d.is_dir() and not d.name.startswith("_") and d.name not in nuevos \
                and ((d / "nuevos.txt").exists() or (d / "originales").is_dir()):
            resultado.append((d.name, True, True))
    return sorted(resultado, key=lambda x: x[0].lower())


def podar_vacios(carpeta):
    """Borra las carpetas que quedaron vacías (de abajo hacia arriba), incluida 'carpeta' si queda vacía."""
    if not carpeta.is_dir():
        return
    for d in sorted((x for x in carpeta.rglob("*") if x.is_dir()), key=lambda x: len(x.parts), reverse=True):
        try:
            d.rmdir()
        except OSError:
            pass
    try:
        carpeta.rmdir()
    except OSError:
        pass


def crear_carpetas(carpeta_juego, carpeta, indice):
    """Crea 'carpeta' y apunta en el índice las que no existían, para poder quitarlas luego si quedan vacías."""
    faltan = []
    c = carpeta
    while not c.exists() and c != carpeta_juego:
        faltan.append(c)
        c = c.parent
    carpeta.mkdir(parents=True, exist_ok=True)
    for c in faltan:
        indice["dir:" + c.relative_to(carpeta_juego).as_posix()] = True


def podar_carpetas_nuevas(carpeta_juego, indice):
    """Quita las carpetas que creó algún mod y que ya están vacías (nunca toca las que ya eran del juego)."""
    for clave in sorted((k for k in indice if k.startswith("dir:")), key=len, reverse=True):
        carpeta = carpeta_juego / clave[4:]
        if carpeta.is_dir():
            try:
                carpeta.rmdir()
            except OSError:
                continue                                  # todavía tiene cosas dentro
        del indice[clave]


def quitar_archivo(carpeta_juego, archivo, indice):
    """Borra un archivo que había añadido un mod (y su versión compilada, que el juego crea solo)."""
    candidatos = [archivo]
    if archivo.suffix.lower() in (".rpy", ".rpym"):
        compilado = archivo.with_suffix(archivo.suffix + "c")          # x.rpy -> x.rpyc
        if compilado.relative_to(carpeta_juego).as_posix() not in indice:   # salvo que sea de otro mod
            candidatos.append(compilado)
    for c in candidatos:
        try:
            c.unlink()
        except FileNotFoundError:
            pass


def reconstruir_archivos(carpeta_juego, claves, infos, indice, excluir=None):
    """Deja cada archivo de 'claves' como debe estar según los mods activos (sin contar 'excluir')."""
    raiz = carpeta_respaldo(carpeta_juego)
    activos = {n: set(i["archivos"]) for n, i in infos.items() if i.get("activo") and n != excluir}
    for clave in claves:
        destino = carpeta_juego / clave
        gana = max((n for n, c in activos.items() if clave in c), key=lambda n: infos[n]["orden"], default=None)
        if gana is not None:
            crear_carpetas(carpeta_juego, destino.parent, indice)
            shutil.copy2(raiz / gana / "archivos" / clave, destino)
        elif indice.get(clave) is True:
            crear_carpetas(carpeta_juego, destino.parent, indice)
            shutil.copy2(raiz / "_base" / clave, destino)
        elif indice.get(clave) is False:
            quitar_archivo(carpeta_juego, destino, indice)
    podar_carpetas_nuevas(carpeta_juego, indice)


def desinstalar_mod_ddlc(carpeta_juego, nombre):
    """Quita un mod de DDLC: borra lo que añadió, devuelve los originales que pisó y olvida sus copias."""
    raiz = carpeta_respaldo(carpeta_juego)
    infos = leer_mods_instalados(carpeta_juego)
    if nombre not in infos:                               # instalado con una versión antigua de Modib
        nuevos = []
        archivo = raiz / nombre / "nuevos.txt"
        if archivo.exists():
            nuevos = [Path(linea) for linea in archivo.read_text(encoding="utf-8").splitlines() if linea.strip()]
        revertir(carpeta_juego, raiz / nombre, nuevos)
        return
    info = infos[nombre]
    indice = leer_indice(carpeta_juego)
    reconstruir_archivos(carpeta_juego, info["archivos"], infos, indice, excluir=nombre)
    shutil.rmtree(raiz / nombre)
    quedan = set()
    for n, i in infos.items():
        if n != nombre:
            quedan |= set(i["archivos"])
    for clave in info["archivos"]:
        if clave not in quedan:                           # ya ningún mod toca este archivo: se olvida
            indice.pop(clave, None)
            try:
                (raiz / "_base" / clave).unlink()
            except OSError:
                pass
    if any(not k.startswith("dir:") for k in indice):
        guardar_indice(carpeta_juego, indice)
    else:
        shutil.rmtree(raiz / "_base", ignore_errors=True)
    podar_vacios(raiz)


# ---------- Trabajo en segundo plano + circulito de espera ----------
def girar():
    fondo.delete("giro")
    if not espera["activo"]:
        return
    x, y = CENTRO_GIRO
    fondo.create_oval(x - 9, y - 9, x + 9, y + 9, outline="#6b6f74", width=3, tags="giro")
    fondo.create_arc(x - 9, y - 9, x + 9, y + 9, start=espera["angulo"], extent=100,
                     style="arc", outline=BLANCO, width=3, tags="giro")
    espera["angulo"] = (espera["angulo"] - 14) % 360
    espera["tarea"] = ventana.after(30, girar)


def mostrar_espera(texto):
    fondo.itemconfig(texto_espera, text=texto)
    if not espera["activo"]:
        espera["activo"] = True
        girar()


def ocultar_espera():
    espera["activo"] = False
    if espera["tarea"] is not None:
        ventana.after_cancel(espera["tarea"])
        espera["tarea"] = None
    fondo.itemconfig(texto_espera, text="")
    fondo.delete("giro")


def trabajar(texto, tarea, al_terminar):
    """Hace 'tarea' en segundo plano (la ventana no se congela) con el circulito girando.
    Al acabar llama a al_terminar(resultado), donde resultado tiene 'valor' o 'error'."""
    if espera["ocupado"]:
        return
    espera["ocupado"] = True
    actualizar()          # bloquea los botones mientras se trabaja
    mostrar_espera(texto)
    resultado = {}

    def hilo():
        try:
            resultado["valor"] = tarea()
        except Exception as e:
            resultado["error"] = e

    t = threading.Thread(target=hilo, daemon=True)
    t.start()

    def comprobar():
        if t.is_alive():
            ventana.after(50, comprobar)
            return
        espera["ocupado"] = False
        ocultar_espera()
        if "error" in resultado:
            error = resultado["error"]
            guardar_error(type(error), error, error.__traceback__)
        actualizar()
        al_terminar(resultado)

    ventana.after(50, comprobar)


# ---------- Acciones de cada paso ----------
def info_launcher():
    """Datos del launcher elegido (solo en juegos con detección automática, como Minecraft)."""
    adaptador = JUEGOS.get(estado["juego"], {})
    return adaptador.get("info_launchers", {}).get(estado["launcher"])


def detectar_carpeta_automatica():
    """Launchers con carpeta fija (.minecraft): la encuentra sola, sin preguntar nada."""
    info = info_launcher()
    if not info or info["tipo"] != "fija":
        return
    encontradas = info["buscar"]()
    if encontradas:
        etiqueta, ruta = encontradas[0]
        estado.update(carpeta=str(ruta), etiqueta=etiqueta)
    else:
        messagebox.showinfo("Modib", tr("launcher_sin_carpeta", launcher=estado["launcher"]))


def paso1():
    nombres = {nombre_launcher(i): i for i in JUEGOS[estado["juego"]]["launchers"]}
    elegido = elegir_flexible(tr("donde_tienes_juego"), list(nombres))
    launcher = nombres.get(elegido, elegido)
    if launcher:
        estado.update(launcher=launcher, carpeta=None, etiqueta=None, mod=None)
        actualizar()
        detectar_carpeta_automatica()
        if estado["carpeta"] is None:
            recuperar_carpeta()          # la que ya habías elegido otra vez, si sigue existiendo
        actualizar()


def elegir_instancia(info):
    """Busca las instancias/perfiles del launcher y deja elegir en cuál instalar."""
    opciones = info["buscar"]()
    if not opciones:
        if messagebox.askyesno("Modib", tr("launcher_no_encontrado", launcher=estado["launcher"])):
            ruta = filedialog.askdirectory(title=tr("titulo_carpeta_launcher", launcher=estado["launcher"]))
            if ruta:
                fijar_carpeta(ruta)
        return
    if len(opciones) == 1:
        etiqueta, ruta = opciones[0]
    else:
        nombres = [e for e, _ in opciones]
        elegido = elegir_flexible(tr("en_que_instalo", item=tr("item_" + info.get("item", "carpeta"))), nombres)
        if elegido is None:
            return
        etiqueta, ruta = opciones[nombres.index(elegido)]
    fijar_carpeta(ruta, etiqueta)


def elegir_a_mano(adaptador):
    ruta = filedialog.askdirectory(title=tr("titulo_carpeta_juego", juego=estado["juego"]))
    if not ruta:
        return
    marcador = adaptador.get("marcador")
    if marcador and not (Path(ruta) / marcador).exists():
        messagebox.showwarning("Modib", tr("no_veo_marcador", marcador=marcador))
        return
    if (Path(ruta) / MARCA_COPIA).exists():
        messagebox.showwarning("Modib", tr("es_copia"))
        return
    fijar_carpeta(ruta)


def buscar_carpeta_automatica(adaptador):
    """Busca el juego por el PC (mientras gira el circulito) y deja elegir si hay varios."""
    def al_terminar(r):
        if "error" in r:
            messagebox.showerror("Modib", tr("no_pude_buscar", error=r["error"]))
            return
        encontrados = r["valor"]
        if not encontrados:
            if messagebox.askyesno("Modib", tr("juego_no_encontrado", juego=estado["juego"])):
                elegir_a_mano(adaptador)
            return
        if len(encontrados) == 1:
            ruta = encontrados[0]
        else:
            elegido = elegir_de_lista(tr("encontre_varias"), [str(c) for c in encontrados])
            if elegido is None:
                return
            ruta = Path(elegido)
        fijar_carpeta(ruta)

    trabajar(tr("buscando"), lambda: buscar_en_el_pc(adaptador["reconocer"]), al_terminar)


def paso2():
    info = info_launcher()
    if info:
        elegir_instancia(info)
        return
    adaptador = JUEGOS[estado["juego"]]
    if "reconocer" in adaptador:
        opcion = elegir(tr("como_busco"), [tr("buscar_auto"), tr("elegir_mano")])
        if opcion is None:
            return
        if opcion == tr("buscar_auto"):
            buscar_carpeta_automatica(adaptador)
            return
    elegir_a_mano(adaptador)


def elegir_jar():
    """Para juegos como Minecraft: el mod es un archivo .jar."""
    ruta = filedialog.askopenfilename(
        title=tr("elige_mod_jar"),
        filetypes=[(tr("tipo_jar"), "*.jar")],
    )
    if not ruta:
        return
    try:
        detectar_loaders(ruta)
    except zipfile.BadZipFile:
        messagebox.showerror("Modib", tr("jar_invalido"))
        return
    estado["mod"] = ruta
    actualizar()


def paso3():
    if JUEGOS[estado["juego"]].get("formato") == "jar":
        elegir_jar()
        return
    tipo = elegir(tr("como_es_mod"), [tr("archivo_zip"), tr("carpeta")])
    if tipo is None:
        return
    if tipo == tr("carpeta"):
        ruta = filedialog.askdirectory(title=tr("carpeta_del_mod"))
    else:
        ruta = filedialog.askopenfilename(
            title=tr("elige_tu_mod"),
            filetypes=[(tr("mods_comprimidos"), "*.zip"), (tr("todos_archivos"), "*.*")],
        )
    if not ruta:
        return

    ruta = Path(ruta)
    if ruta.suffix.lower() != ".zip":
        if ruta.is_file():
            messagebox.showinfo("Modib", tr("solo_zip_o_carpeta"))
            return
        clasificaciones.clear()
        estado["mod"] = str(ruta)
        actualizar()
        return

    def al_terminar(r):
        if "error" in r:
            if isinstance(r["error"], zipfile.BadZipFile):
                messagebox.showerror("Modib", tr("zip_invalido"))
            else:
                messagebox.showerror("Modib", tr("no_pude_descomprimir", error=r["error"]))
            return
        clasificaciones.clear()
        estado["mod"] = str(r["valor"])
        actualizar()

    modo = JUEGOS[estado["juego"]]["modo"]
    trabajar(tr("descomprimiendo"), lambda: descomprimir(ruta, modo), al_terminar)


def paso4():
    carpeta_juego = Path(estado["carpeta"])
    mod = Path(estado["mod"])
    if JUEGOS[estado["juego"]]["modo"] == "fusionar":
        organizar_fusionando(carpeta_juego, mod)
    else:
        organizar_en_carpeta(carpeta_juego, mod)


def organizar_fusionando(carpeta_juego, mod):
    """DDLC: crea una copia del juego para este mod (o, si es un complemento, lo añade a la copia que elijas)."""
    try:
        info = clasificar_mod_fusion(mod)
    except OSError as e:
        messagebox.showerror("Modib", tr("no_pude_instalar", error=e))
        return
    if info is None:
        messagebox.showerror("Modib", tr("no_reconozco_mod"))
        return
    if "steamapps" in [parte.lower() for parte in carpeta_juego.parts] and \
            not messagebox.askyesno("Modib", tr("aviso_steam")):
        return
    if listar_mods_ddlc(carpeta_juego) and not messagebox.askyesno("Modib", tr("aviso_antiguas")):
        return

    nombre_copia = None
    if info["complemento"]:
        copias = listar_copias(carpeta_juego)
        if copias:
            nueva = tr("copia_nueva")
            elegido = elegir_flexible(tr("donde_lo_instalo", mod=mod.name), [c["nombre"] for c in copias] + [nueva])
            if elegido is None:
                return
            if elegido != nueva:
                nombre_copia = elegido

    if nombre_copia:
        if not messagebox.askyesno("Modib", tr("confirmar_complemento", mod=mod.name, copia=nombre_copia)):
            return
        tarea = lambda: instalar_complemento(mod, carpeta_juego, info, nombre_copia)
    else:
        destino = carpeta_copias(carpeta_juego) / mod.name
        if destino.exists():
            messagebox.showwarning("Modib", tr("ya_instalado", mod=mod.name))
            return
        pregunta = tr("confirmar_copia", mb=espacio_necesario(carpeta_juego, info) // (1024 * 1024) + 1, ruta=destino)
        if info["popular"]:
            pregunta = tr("popular", nombre=info["popular"]) + "\n\n" + pregunta
        if not messagebox.askyesno("Modib", pregunta):
            return
        tarea = lambda: instalar_ddlc_copia(mod, carpeta_juego, info)

    def al_terminar(r):
        if "error" in r:
            messagebox.showerror("Modib", tr("no_pude_instalar", error=r["error"]))
            return
        if r["valor"]["copia"]:
            mensaje = tr("instalado_complemento", mod=mod.name, copia=r["valor"]["copia"])
        else:
            mensaje = tr("instalado_copia", mod=mod.name, ruta=r["valor"]["destino"])
        messagebox.showinfo("Modib", mensaje + "\n\n" + tr("consejo_errores"))
        estado["mod"] = None
        actualizar()

    trabajar(tr("instalando"), tarea, al_terminar)


def organizar_en_carpeta(carpeta_juego, mod):
    carpeta_mods = carpeta_juego / CARPETA_MODS
    destino = carpeta_mods / mod.name

    loaders = []
    if mod.suffix.lower() == ".jar":
        try:
            loaders = detectar_loaders(mod)
        except Exception:
            loaders = []

    if (destino.exists() or (carpeta_juego / CARPETA_DESACTIVADOS / mod.name).exists()
            or (carpeta_mods / (mod.name + ".disabled")).exists()):
        messagebox.showwarning("Modib", tr("ya_en_juego", mod=mod.name))
        return

    # Nota final para los launchers que descargan mods por sí mismos
    nota = ""
    info = info_launcher()
    if info and info.get("descarga"):
        como = "" if estado["launcher"] == "Prism Launcher" else tr("como_prism")
        nota = "\n\n" + tr("nota_descarga", launcher=estado["launcher"], como=como)

    def al_terminar(r):
        if "error" in r:
            messagebox.showerror("Modib", tr("no_pude_copiar", error=r["error"]))
            return
        mensaje = tr("listo_copiado", mod=mod.name, destino=destino)
        if mod.suffix.lower() == ".jar":
            if loaders:
                mensaje += "\n\n" + tr("es_mod_de", loaders=" / ".join(loaders))
            else:
                mensaje += "\n\n" + tr("loader_desconocido")
        messagebox.showinfo("Modib", mensaje + nota)
        estado["mod"] = None  # así puedes añadir otro mod enseguida
        actualizar()

    trabajar(tr("organizando"), lambda: copiar_mod(mod, destino, carpeta_mods), al_terminar)


acciones = [paso1, paso2, paso3, paso4]

# ---------- Dibujo ----------
Y_ICONOS = 100

# Un solo lienzo que ocupa toda la ventana: aquí se dibuja el fondo de cada juego,
# los hexágonos, los textos y (encima) los botones.
fondo = tk.Canvas(ventana, width=ANCHO, height=ALTO, bg=FONDO, highlightthickness=0)

botones, subtitulos = [], []
for i in range(N):
    cx = COL * i + COL // 2
    b = crear_boton(fondo, textos_pasos()[i], acciones[i])
    fondo.create_window(cx, 182, window=b)
    botones.append(b)
    subtitulos.append(fondo.create_text(cx, 218, text="", fill="#c8cacc", font=("Segoe UI", 9),
                                        width=COL - 10, anchor="n"))

texto_pie = fondo.create_text(ANCHO // 2, 358, text=tr("pie", version=VERSION), fill="#c8cacc",
                              font=("Segoe UI", 9))

# Botones de arriba: volver a la lista de juegos, ver tus mods, y el nombre del juego
boton_volver = crear_boton_chico(fondo, tr("btn_juegos"), lambda: volver_a_juegos())
fondo.create_window(70, 24, window=boton_volver)
boton_mods = crear_boton_chico(fondo, tr("btn_mis_mods"), lambda: abrir_mods())
fondo.create_window(ANCHO - 70, 24, window=boton_mods)
titulo_juego = fondo.create_text(ANCHO // 2, 24, text="", fill=BLANCO, font=("Segoe UI", 15, "bold"))

# Circulito de espera (abajo, pequeño)
CENTRO_GIRO = (ANCHO // 2 - 50, 322)
texto_espera = fondo.create_text(CENTRO_GIRO[0] + 18, CENTRO_GIRO[1], text="", fill="#c8cacc",
                                 font=("Segoe UI", 9), anchor="w")


# ---------- Un fondo distinto para cada juego ----------
def mezclar(color, fuerza):
    """Mezcla un color con el fondo gris. fuerza 0 = invisible, 1 = color completo."""
    c = [int(color[k:k + 2], 16) for k in (1, 3, 5)]
    f = [int(FONDO[k:k + 2], 16) for k in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(f[k] + (c[k] - f[k]) * fuerza) for k in range(3))


imagenes = {}  # guardamos las imágenes aquí para que Tk no las pierda


def baldosa_pasto(semilla):
    """Un bloque de pasto de 16x16 'píxeles', ampliado x4 y suave."""
    azar = random.Random(semilla)
    verdes = ["#5d9b3a", "#6aa84f", "#528a32", "#74b857"]
    tierras = ["#866043", "#79553a", "#6b4a2f", "#8a6a4a"]
    filas = []
    for y in range(16):
        fila = []
        for x in range(16):
            if x == 15 or y == 15:  # línea oscura entre bloques
                base = "#2f2a22"
            elif y < 4:
                base = azar.choice(verdes)
            elif y < 6:  # el borde irregular donde el pasto se mezcla con la tierra
                base = azar.choice(verdes) if azar.random() < (0.65 if y == 4 else 0.25) else azar.choice(tierras)
            else:
                base = azar.choice(tierras)
            fila.append(mezclar(base, 0.22))
        filas.append("{" + " ".join(fila) + "}")
    img = tk.PhotoImage(width=16, height=16)
    img.put(" ".join(filas))
    return img.zoom(4)


def pintar_minecraft():
    if "pasto" not in imagenes:
        imagenes["pasto"] = [baldosa_pasto(7), baldosa_pasto(11), baldosa_pasto(23)]
    azar = random.Random(3)
    for y in range(0, ALTO, 64):
        for x in range(0, ANCHO, 64):
            fondo.create_image(x, y, image=azar.choice(imagenes["pasto"]), anchor="nw", tags="arte")


# Fondos de FNF y DDLC: una "baldosa" (imagen PNG incrustada como texto) que se repite por toda la ventana.
# Los dibujos son: micrófonos (FNF) y el lazo de Sayori, el lápiz de Monika, el cupcake de Natsuki y el cuchillo de Yuri (DDLC).
# Fondos de FNF y DDLC: un dibujo del tamaño de la ventana, guardado en la carpeta 'assets' (junto al programa;
# dentro del .exe va empaquetado con --add-data). Si falta el archivo, no se dibuja el fondo y el programa funciona igual.
RECURSOS = Path(getattr(sys, "_MEIPASS", BASE)) / "assets"


def pintar_fondo_imagen(clave, archivo):
    """Dibuja una imagen que cubre toda la ventana, detrás de todo lo demás."""
    if clave not in imagenes:
        try:
            imagenes[clave] = tk.PhotoImage(file=str(RECURSOS / archivo))
        except tk.TclError:
            imagenes[clave] = None
    if imagenes[clave] is not None:
        fondo.create_image(0, 0, image=imagenes[clave], anchor="nw", tags="arte")


def pintar_fnf():
    pintar_fondo_imagen("fnf", "fondo_fnf.png")


def pintar_ddlc():
    pintar_fondo_imagen("ddlc", "fondo_ddlc.png")


FONDOS = {"Minecraft": pintar_minecraft, "Friday Night Funkin'": pintar_fnf, "DDLC": pintar_ddlc}
tema = {"actual": "sin definir"}


def aplicar_fondo():
    """Cambia el fondo cuando eliges otro juego (los que no tienen fondo propio quedan lisos)."""
    juego = estado["juego"]
    if tema["actual"] == juego:
        return
    tema["actual"] = juego
    fondo.delete("arte")
    if juego in FONDOS:
        FONDOS[juego]()
        fondo.tag_lower("arte")  # el dibujo siempre queda por detrás de todo lo demás


def dibujar_iconos(actual):
    fondo.delete("iconos")
    cy = Y_ICONOS
    for i in range(N):
        cx = COL * i + COL // 2
        color = BLANCO if i <= actual else "#6b6f74"
        puntos = []
        for k in range(6):
            ang = math.radians(60 * k - 90)
            puntos += [cx + 28 * math.cos(ang), cy + 28 * math.sin(ang)]
        fondo.create_polygon(puntos, fill=color, outline=color, tags="iconos")
        fondo.create_text(cx, cy, text="✓" if i < actual else str(i + 1), fill=FONDO,
                          font=("Segoe UI", 15, "bold"), tags="iconos")
        if i < N - 1:
            lc = "#9a9ea3" if i < actual else "#6b6f74"
            fondo.create_line(cx + 45, cy, cx + COL - 45, cy, fill=lc, width=2, tags="iconos")


def actualizar():
    aplicar_fondo()
    valores = [estado["launcher"], estado["carpeta"], estado["mod"]]
    actual = next((i for i, v in enumerate(valores) if v is None), N - 1)
    dibujar_iconos(actual)

    # El paso 2 se llama "Elegir instancia" o "Elegir perfil" en launchers que tienen varias
    textos = textos_pasos()
    info = info_launcher()
    if info and info["tipo"] != "fija":
        textos[1] = tr("paso_" + info.get("item", "carpeta"))

    # Mientras se trabaja, los botones se bloquean
    bloqueo = "disabled" if espera["ocupado"] else "normal"

    for i in range(N):
        b = botones[i]
        if i == actual:
            b.config(state=bloqueo, bg=AZUL, fg=BLANCO, text=textos[i])
        elif i < actual:
            b.config(state=bloqueo, bg=GRIS_HECHO, fg=BLANCO, text=tr("cambiar"))
        else:
            b.config(state="disabled", bg=GRIS_OFF, text=textos[i])

    nombre_mod = None
    if estado["mod"]:
        ruta_mod = Path(estado["mod"])
        nombre_mod = ruta_mod.name
        if CARPETA_TEMP in ruta_mod.parents:
            nombre_mod += " " + tr("descomprimido")
        if JUEGOS.get(estado["juego"], {}).get("modo") == "fusionar":
            nombre_mod += "\n" + etiqueta_mod_fusion(ruta_mod)   # por ejemplo: "solo skins"

    nombres = [
        nombre_launcher(estado["launcher"]) if estado["launcher"] else None,
        (estado.get("etiqueta") or os.path.basename(estado["carpeta"])) if estado["carpeta"] else None,
        nombre_mod,
        "",
    ]
    for i in range(N):
        fondo.itemconfig(subtitulos[i], text=nombres[i] or "")

    fondo.itemconfig(titulo_juego, text=estado["juego"] or "")
    ocupado = espera["ocupado"]
    boton_volver.config(state="disabled" if ocupado else "normal")
    hay_carpeta = bool(estado["carpeta"]) and not ocupado
    boton_mods.config(state="normal" if hay_carpeta else "disabled",
                      bg=GRIS_HECHO if hay_carpeta else GRIS_OFF)


# ======================================================================
#  PANTALLA 1: elegir el juego (una cuadrícula de cuadrados)
# ======================================================================
LADO = 120        # tamaño de cada cuadrado
SEP = 24          # espacio entre cuadrados
COLUMNAS = 4
ANCHO_LIENZO = ANCHO - 48 - 18
ALTO_LIENZO = ALTO - 76

pantalla_juegos = tk.Frame(ventana, bg=FONDO)
etiqueta_elige = tk.Label(pantalla_juegos, text=tr("elige_juego"), bg=FONDO, fg=BLANCO,
                          font=("Segoe UI", 18, "bold"))
etiqueta_elige.pack(pady=(16, 6))
boton_acerca = crear_boton_chico(pantalla_juegos, tr("btn_acerca"), lambda: mostrar_acerca(), ancho=12)
boton_acerca.place(x=24, y=14)
boton_idioma = crear_boton_chico(pantalla_juegos, tr("btn_idioma", nombre=IDIOMAS["es"]), lambda: mostrar("idioma"), ancho=18)
boton_idioma.place(x=ANCHO - 24, y=14, anchor="ne")
marco_juegos = tk.Frame(pantalla_juegos, bg=FONDO)
marco_juegos.pack(fill="both", expand=True, padx=24, pady=(0, 14))
lienzo_juegos = tk.Canvas(marco_juegos, width=ANCHO_LIENZO, height=ALTO_LIENZO, bg=FONDO, highlightthickness=0)
barra_juegos = tk.Scrollbar(marco_juegos, orient="vertical", command=lienzo_juegos.yview)
lienzo_juegos.configure(yscrollcommand=barra_juegos.set)
lienzo_juegos.pack(side="left")


# Iconos minimalistas de cada juego (cx, cy = centro del dibujo)
def icono_minecraft(c, cx, cy, tag):
    """Un bloque de pasto: cuadrado de 8x8 'píxeles'."""
    azar = random.Random(5)
    verdes = ["#5d9b3a", "#6aa84f", "#528a32", "#74b857"]
    tierras = ["#866043", "#79553a", "#6b4a2f", "#8a6a4a"]
    celda = 8
    x0, y0 = cx - 4 * celda, cy - 4 * celda
    for fila in range(8):
        for col in range(8):
            if fila < 2:
                color = azar.choice(verdes)
            elif fila == 2:
                color = azar.choice(verdes) if azar.random() < 0.5 else azar.choice(tierras)
            else:
                color = azar.choice(tierras)
            c.create_rectangle(x0 + col * celda, y0 + fila * celda, x0 + (col + 1) * celda, y0 + (fila + 1) * celda,
                               fill=color, outline="", tags=tag)


def icono_fnf(c, cx, cy, tag):
    """Un micrófono."""
    r = 17
    hy = cy - 14  # centro de la cabeza
    c.create_rectangle(cx - 5, hy + r, cx + 5, cy + 32, fill="#9aa0a6", outline="", tags=tag)         # mango
    c.create_rectangle(cx - 9, hy + r + 4, cx + 9, hy + r + 9, fill="#2b2d31", outline="", tags=tag)   # anillo
    c.create_oval(cx - r, hy - r, cx + r, hy + r, fill="#e8eaed", outline="#2b2d31", width=3, tags=tag)  # cabeza
    for d in (-9, 0, 9):                                                                             # rejilla
        mitad = int((r * r - d * d) ** 0.5) - 3
        c.create_line(cx - mitad, hy + d, cx + mitad, hy + d, fill="#2b2d31", width=2, tags=tag)
        c.create_line(cx + d, hy - mitad, cx + d, hy + mitad, fill="#2b2d31", width=2, tags=tag)


def icono_ddlc(c, cx, cy, tag):
    """Un corazón."""
    rosa = "#ff8fb1"
    c.create_oval(cx - 27, cy - 24, cx + 1, cy + 4, fill=rosa, outline="", tags=tag)
    c.create_oval(cx - 1, cy - 24, cx + 27, cy + 4, fill=rosa, outline="", tags=tag)
    c.create_polygon([cx - 26, cy - 5, cx + 26, cy - 5, cx, cy + 28], fill=rosa, outline="", tags=tag)


ICONOS = {"Minecraft": icono_minecraft, "Friday Night Funkin'": icono_fnf, "DDLC": icono_ddlc}


def dibujar_juegos():
    lienzo_juegos.delete("all")
    ancho_grid = COLUMNAS * LADO + (COLUMNAS - 1) * SEP
    x0 = (ANCHO_LIENZO - ancho_grid) // 2
    juegos = list(JUEGOS)
    for idx, juego in enumerate(juegos):
        fila, col = divmod(idx, COLUMNAS)
        x = x0 + col * (LADO + SEP)
        y = 6 + fila * (LADO + SEP)
        tag = f"juego{idx}"
        marco = lienzo_juegos.create_rectangle(x, y, x + LADO, y + LADO, fill=GRIS_OFF, outline=GRIS_OFF,
                                               width=3, tags=tag)
        icono = ICONOS.get(juego)
        if icono:
            icono(lienzo_juegos, x + LADO // 2, y + 50, tag)
        lienzo_juegos.create_text(x + LADO // 2, y + LADO - 18, text=JUEGOS[juego].get("corto", juego),
                                  fill=BLANCO, font=("Segoe UI", 11, "bold"), tags=tag)
        lienzo_juegos.tag_bind(tag, "<Button-1>", lambda e, j=juego: elegir_juego(j))
        lienzo_juegos.tag_bind(tag, "<Enter>", lambda e, m=marco: (
            lienzo_juegos.itemconfig(m, outline=AZUL), lienzo_juegos.config(cursor="hand2")))
        lienzo_juegos.tag_bind(tag, "<Leave>", lambda e, m=marco: (
            lienzo_juegos.itemconfig(m, outline=GRIS_OFF), lienzo_juegos.config(cursor="")))

    filas = (len(juegos) + COLUMNAS - 1) // COLUMNAS
    alto_total = 6 + filas * (LADO + SEP)
    lienzo_juegos.configure(scrollregion=(0, 0, ANCHO_LIENZO, alto_total))
    if alto_total > ALTO_LIENZO:           # la barra solo aparece si hacen falta
        barra_juegos.pack(side="left", fill="y")
    else:
        barra_juegos.pack_forget()


def elegir_juego(juego):
    if juego != estado["juego"]:
        estado.update(juego=juego, launcher=None, carpeta=None, etiqueta=None, mod=None)
    actualizar()
    mostrar("pasos")


def volver_a_juegos():
    if espera["ocupado"]:
        return
    mostrar("juegos")


# ======================================================================
#  PANTALLA 3: lista de mods con botones de activar / desactivar
# ======================================================================
pantalla_mods = tk.Frame(ventana, bg=FONDO)
cabecera_mods = tk.Frame(pantalla_mods, bg=FONDO)
cabecera_mods.pack(fill="x", padx=24, pady=(14, 8))
boton_volver_mods = crear_boton_chico(cabecera_mods, tr("btn_volver"), lambda: mostrar("pasos"))
boton_volver_mods.pack(side="left")
titulo_mods = tk.Label(cabecera_mods, text="", bg=FONDO, fg=BLANCO, font=("Segoe UI", 13, "bold"))
titulo_mods.pack(side="left", padx=16)
boton_abrir_carpeta = crear_boton_chico(cabecera_mods, tr("btn_abrir_carpeta"), lambda: abrir_carpeta_mods(), ancho=13)
boton_abrir_carpeta.pack(side="right")
boton_refrescar = crear_boton_chico(cabecera_mods, tr("btn_actualizar"), lambda: refrescar_mods(), ancho=12)
boton_refrescar.pack(side="right", padx=(0, 8))
resumen_mods = tk.Label(pantalla_mods, text="", bg=FONDO, fg="#c8cacc", font=("Segoe UI", 10), anchor="w")
resumen_mods.pack(fill="x", padx=26)

marco_mods = tk.Frame(pantalla_mods, bg=FONDO)
marco_mods.pack(fill="both", expand=True, padx=24, pady=(0, 16))
lienzo_mods = tk.Canvas(marco_mods, bg=FONDO, highlightthickness=0)
barra_mods = tk.Scrollbar(marco_mods, orient="vertical", command=lienzo_mods.yview)
lienzo_mods.configure(yscrollcommand=barra_mods.set)
barra_mods.pack(side="right", fill="y")
lienzo_mods.pack(side="left", fill="both", expand=True)
interior_mods = tk.Frame(lienzo_mods, bg=FONDO)
lienzo_mods.create_window(0, 0, window=interior_mods, anchor="nw", width=ANCHO - 48 - 24)
interior_mods.bind("<Configure>", lambda e: lienzo_mods.configure(scrollregion=lienzo_mods.bbox("all")))


def listar_mods(carpeta_juego, juego):
    """Devuelve [(nombre, ruta, activo)] con los mods instalados, ordenados por nombre."""
    carpeta_mods = carpeta_juego / CARPETA_MODS
    mods = []
    if JUEGOS[juego].get("formato") == "jar":
        # Minecraft: un mod apagado es un .jar que termina en ".jar.disabled" (igual que hacen Prism y otros)
        if carpeta_mods.is_dir():
            for f in carpeta_mods.iterdir():
                bajo = f.name.lower()
                if f.is_file() and bajo.endswith(".jar"):
                    mods.append((f.name[:-4], f, True))
                elif f.is_file() and bajo.endswith(".jar.disabled"):
                    mods.append((f.name[:-13], f, False))
    else:
        # FNF y otros: un mod apagado es una carpeta que está en "mods_desactivados"
        for carpeta, activo in ((carpeta_mods, True), (carpeta_juego / CARPETA_DESACTIVADOS, False)):
            if carpeta.is_dir():
                for f in carpeta.iterdir():
                    if f.is_dir():
                        mods.append((f.name, f, activo))
    return sorted(mods, key=lambda x: x[0].lower())


def alternar_mod(ruta, activo, juego, carpeta_juego):
    """Activa o desactiva un mod sin borrar nada. Devuelve el texto de un error, o None si salió bien."""
    if JUEGOS[juego].get("formato") == "jar":
        nuevo = ruta.with_name(ruta.name + ".disabled") if activo else ruta.with_name(ruta.name[:-len(".disabled")])
    else:
        nuevo = carpeta_juego / (CARPETA_DESACTIVADOS if activo else CARPETA_MODS) / ruta.name
    if nuevo.exists():
        return tr("ya_existe_destino", nombre=nuevo.name)
    try:
        nuevo.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(ruta), str(nuevo))
    except OSError as e:
        return tr("no_pude_cambiar", error=e)
    return None


def cambiar_estado_mod(ruta, activo):
    error = alternar_mod(ruta, activo, estado["juego"], Path(estado["carpeta"]))
    if error:
        messagebox.showerror("Modib", error)
    posicion = lienzo_mods.yview()[0]
    llenar_mods()
    ventana.update_idletasks()
    lienzo_mods.yview_moveto(posicion)   # la lista se queda donde estaba


def jugar_ddlc(copia):
    """Abre el juego de esa copia (con el .exe del mod si lo tiene)."""
    ejecutables = copia.get("ejecutables") or ["DDLC.exe"]
    exe = ejecutables[0]
    if len(ejecutables) > 1:
        exe = elegir_flexible(tr("elige_ejecutable"), ejecutables)
        if exe is None:
            return
    try:
        subprocess.Popen([str(copia["ruta"] / exe)], cwd=str(copia["ruta"]))
    except OSError as e:
        messagebox.showerror("Modib", tr("no_pude_abrir", error=e))


def abrir_carpeta_de(ruta):
    try:
        os.startfile(str(ruta))
    except (AttributeError, OSError):
        messagebox.showinfo("Modib", tr("carpeta_esta_en", ruta=ruta))


def hacer_con_espera(accion):
    """Ejecuta 'accion' mostrando el cursor de espera y avisa si falla. Después refresca la lista."""
    ventana.config(cursor="watch")
    ventana.update_idletasks()
    try:
        accion()
    except (OSError, KeyError, ValueError) as e:
        messagebox.showerror("Modib", tr("no_pude_cambiar", error=e))
    finally:
        ventana.config(cursor="")
    refrescar_mods()


def eliminar_ddlc(nombre):
    if messagebox.askyesno("Modib", tr("confirmar_eliminar", mod=nombre)):
        hacer_con_espera(lambda: eliminar_copia(Path(estado["carpeta"]), nombre))


def deshacer_ddlc(nombre):
    if messagebox.askyesno("Modib", tr("confirmar_deshacer", mod=nombre)):
        hacer_con_espera(lambda: desinstalar_mod_ddlc(Path(estado["carpeta"]), nombre))


def llenar_mods_fusion():
    """Lista de mods de DDLC: cada uno en su copia, con Jugar, Carpeta y Eliminar."""
    carpeta = Path(estado["carpeta"])
    copias = listar_copias(carpeta)
    antiguas = listar_mods_ddlc(carpeta)
    resumen_mods.config(text=tr("resumen_copias", n=len(copias)))
    if not copias and not antiguas:
        tk.Label(interior_mods, text=tr("sin_mods"), bg=FONDO, fg="#c8cacc",
                 font=("Segoe UI", 11)).pack(pady=50)
        return
    for copia in copias:
        fila = tk.Frame(interior_mods, bg=GRIS_OFF)
        fila.pack(fill="x", pady=3)
        crear_boton_chico(fila, tr("btn_eliminar"), lambda n=copia["nombre"]: eliminar_ddlc(n),
                          bg="#7a3b3b", ancho=9).pack(side="right", padx=(0, 10), pady=6)
        crear_boton_chico(fila, tr("btn_carpeta"), lambda r=copia["ruta"]: abrir_carpeta_de(r),
                          ancho=9).pack(side="right", padx=8, pady=6)
        crear_boton_chico(fila, tr("btn_jugar"), lambda c=copia: jugar_ddlc(c),
                          bg=AZUL, ancho=9).pack(side="right", pady=6)
        textos = tk.Frame(fila, bg=GRIS_OFF)
        textos.pack(side="left", padx=12, pady=6)
        tipo = copia.get("tipo")
        detalle = tr("tipo_" + tipo) if tipo in ("independiente", "moderno", "clasico") else ""
        if copia.get("popular"):
            detalle = tr("popular", nombre=copia["popular"]) + ("  ·  " + detalle if detalle else "")
        tk.Label(textos, text=copia["nombre"], bg=GRIS_OFF, fg=BLANCO, font=("Segoe UI", 11), anchor="w").pack(anchor="w")
        if detalle:
            tk.Label(textos, text=detalle, bg=GRIS_OFF, fg="#c8cacc", font=("Segoe UI", 9), anchor="w").pack(anchor="w")
    if antiguas:
        tk.Label(interior_mods, text=tr("seccion_antiguas"), bg=FONDO, fg="#c8cacc",
                 font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", pady=(14, 2))
        for nombre, _activo, _antiguo in antiguas:
            fila = tk.Frame(interior_mods, bg=GRIS_OFF)
            fila.pack(fill="x", pady=3)
            crear_boton_chico(fila, tr("btn_deshacer"), lambda n=nombre: deshacer_ddlc(n),
                              bg="#7a3b3b", ancho=9).pack(side="right", padx=10, pady=6)
            tk.Label(fila, text=nombre + " " + tr("antiguo"), bg=GRIS_OFF, fg=TEXTO_OFF,
                     font=("Segoe UI", 11), anchor="w").pack(side="left", padx=12, pady=8)


def llenar_mods():
    for hijo in interior_mods.winfo_children():
        hijo.destroy()
    juego = estado["juego"]

    if JUEGOS[juego]["modo"] == "fusionar":
        llenar_mods_fusion()
        return

    mods = listar_mods(Path(estado["carpeta"]), juego)
    activos = sum(1 for _, _, activo in mods if activo)
    resumen_mods.config(text=tr("resumen_mods", activos=activos, inactivos=len(mods) - activos))
    if not mods:
        tk.Label(interior_mods, text=tr("sin_mods"), bg=FONDO, fg="#c8cacc",
                 font=("Segoe UI", 11)).pack(pady=50)
        return

    for nombre, ruta, activo in mods:
        fila = tk.Frame(interior_mods, bg=GRIS_OFF)
        fila.pack(fill="x", pady=3)
        boton = crear_boton_chico(fila, tr("btn_desactivar") if activo else tr("btn_activar"),
                                  lambda r=ruta, a=activo: cambiar_estado_mod(r, a),
                                  bg=GRIS_HECHO if activo else AZUL)
        boton.pack(side="right", padx=10, pady=6)
        tk.Label(fila, text=tr("estado_activo") if activo else tr("estado_desactivado"), bg=GRIS_OFF,
                 fg="#6fcf97" if activo else TEXTO_OFF, font=("Segoe UI", 9, "bold"),
                 width=13).pack(side="right")
        tk.Label(fila, text=nombre, bg=GRIS_OFF, fg=BLANCO if activo else TEXTO_OFF,
                 font=("Segoe UI", 11), anchor="w").pack(side="left", padx=12, pady=8)


def carpeta_de_mods_del_juego():
    carpeta = Path(estado["carpeta"])
    if JUEGOS[estado["juego"]]["modo"] == "fusionar":              # DDLC: la carpeta donde están las copias de los mods
        return carpeta_copias(carpeta) if carpeta_copias(carpeta).is_dir() else carpeta
    return carpeta / CARPETA_MODS if (carpeta / CARPETA_MODS).is_dir() else carpeta


def abrir_carpeta_mods():
    """Abre en el explorador la carpeta donde están los mods."""
    ruta = carpeta_de_mods_del_juego()
    try:
        os.startfile(str(ruta))
    except (AttributeError, OSError):
        messagebox.showinfo("Modib", tr("carpeta_esta_en", ruta=ruta))


def refrescar_mods():
    """Vuelve a mirar la carpeta (por si añadiste o quitaste mods a mano)."""
    posicion = lienzo_mods.yview()[0]
    llenar_mods()
    ventana.update_idletasks()
    lienzo_mods.yview_moveto(posicion)


def titulo_de_mods():
    lugar = estado["juego"] + (f" · {estado['etiqueta']}" if estado.get("etiqueta") else "")
    return tr("mis_mods", lugar=lugar)


def abrir_mods():
    if not estado["carpeta"]:
        return
    titulo_mods.config(text=titulo_de_mods())
    llenar_mods()
    lienzo_mods.yview_moveto(0)
    mostrar("mods")


# ======================================================================
#  PANTALLA 0: elegir el idioma (la primera vez, y cuando pulsas el botón de idioma)
# ======================================================================
pantalla_idioma = tk.Frame(ventana, bg=FONDO)
tk.Label(pantalla_idioma, text="Elige tu idioma\nChoose your language\nEscolha seu idioma", bg=FONDO, fg=BLANCO,
         font=("Segoe UI", 16, "bold"), justify="center").pack(pady=(40, 22))
for _cod, _nombre in IDIOMAS.items():
    crear_boton(pantalla_idioma, _nombre, lambda c=_cod: elegir_idioma(c)).pack(pady=7, ipadx=30)


def establecer_idioma(cod):
    if cod in IDIOMAS:
        idioma_actual["cod"] = cod


def guardar_idioma(cod):
    datos = cargar_config()
    datos["idioma"] = cod
    guardar_config(datos)


def aplicar_idioma():
    """Pone todos los textos que ya están en pantalla en el idioma elegido."""
    boton_volver.config(text=tr("btn_juegos"))
    boton_mods.config(text=tr("btn_mis_mods"))
    etiqueta_elige.config(text=tr("elige_juego"))
    boton_acerca.config(text=tr("btn_acerca"))
    boton_idioma.config(text=tr("btn_idioma", nombre=IDIOMAS[idioma_actual["cod"]]))
    boton_volver_mods.config(text=tr("btn_volver"))
    boton_abrir_carpeta.config(text=tr("btn_abrir_carpeta"))
    boton_refrescar.config(text=tr("btn_actualizar"))
    fondo.itemconfig(texto_pie, text=tr("pie", version=VERSION))
    actualizar()
    if estado["juego"] and estado["carpeta"]:       # la lista de mods, si ya estaba preparada
        titulo_mods.config(text=titulo_de_mods())
        llenar_mods()


def elegir_idioma(cod):
    establecer_idioma(cod)
    guardar_idioma(cod)
    aplicar_idioma()
    mostrar("juegos")


def mostrar_acerca():
    messagebox.showinfo("Modib", tr("acerca", version=VERSION))


# ======================================================================
#  Cambiar entre pantallas
# ======================================================================
pantallas = {"idioma": pantalla_idioma, "juegos": pantalla_juegos, "pasos": fondo, "mods": pantalla_mods}
pantalla_actual = {"nombre": "idioma"}


def mostrar(nombre):
    for n, widget in pantallas.items():
        if n == nombre:
            widget.place(x=0, y=0, width=ANCHO, height=ALTO)
        else:
            widget.place_forget()
    pantalla_actual["nombre"] = nombre


def rueda_del_raton(evento):
    lienzo = {"juegos": lienzo_juegos, "mods": lienzo_mods}.get(pantalla_actual["nombre"])
    if lienzo is not None:
        lienzo.yview_scroll(int(-1 * (evento.delta / 120)), "units")


ventana.bind_all("<MouseWheel>", rueda_del_raton)


def tecla_escape(evento=None):
    """Esc: de la lista de mods vuelve a los pasos, y de los pasos a la lista de juegos."""
    if espera["ocupado"]:
        return
    if pantalla_actual["nombre"] == "mods":
        mostrar("pasos")
    elif pantalla_actual["nombre"] == "pasos":
        mostrar("juegos")
    elif pantalla_actual["nombre"] == "idioma" and cargar_config().get("idioma") in IDIOMAS:
        mostrar("juegos")


ventana.bind("<Escape>", tecla_escape)


migrar_archivos_viejos()
limpiar_temporales()
actualizar()
dibujar_juegos()


def iniciar():
    """Si ya elegiste idioma antes, entra directo a la lista de juegos; si no, lo pregunta."""
    cod = cargar_config().get("idioma")
    if cod in IDIOMAS:
        establecer_idioma(cod)
        aplicar_idioma()
        mostrar("juegos")
    else:
        mostrar("idioma")


iniciar()
ventana.mainloop()
