# 📖 Bíblia ACF — App Windows (Python)

Aplicativo desktop para Windows da Bíblia Almeida Corrigida Fiel,  
recriado em Python com base no projeto React Native/Expo original.

---

## ✨ Funcionalidades

- 📚 **66 livros** da Bíblia (AT e NT) com busca e filtros
- 📖 Navegação **Livro → Capítulo → Versículo**
- ✅ **Marcar capítulos** como lidos
- 🌓 **Tema claro/escuro** persistente
- 👤 **Perfil** com nome personalizado
- 📊 **Progresso de leitura** por livro e global
- ⬅️ Navegação entre capítulos sem voltar ao menu

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.11+ | Linguagem principal |
| Tkinter (built-in) | Interface gráfica |
| SQLite (built-in) | Banco de dados local |
| Pillow (opcional) | Suporte a ícones/imagens |

> Tkinter e SQLite já vêm com o Python — **não precisa instalar nada extra**!

---

## 🚀 Como executar

### 1. Pré-requisito

Instale o [Python 3.11+](https://www.python.org/downloads/) (marque "Add to PATH").

### 2. Clone ou baixe o projeto

```
Bíblia_ACF_Windows/
├── main.py
├── data/               ← banco SQLite criado aqui automaticamente
│   └── biblia_acf.json ← (opcional) texto completo ACF
├── src/
│   ├── database/db.py
│   ├── context/theme.py
│   └── screens/
│       ├── home_screen.py
│       ├── chapters_screen.py
│       ├── verse_list.py
│       └── profile_screen.py
└── README.md
```

### 3. Execute

```bash
python main.py
```

---

## 📖 Texto completo da Bíblia (ACF)

O app usa um texto de demonstração por padrão.  
Para o texto **completo** da ACF, adicione o arquivo:

```
data/biblia_acf.json
```

No formato:

```json
{
  "Gênesis": {
    "1": ["versículo 1...", "versículo 2...", ...],
    "2": ["...", ...]
  },
  "Êxodo": { ... }
}
```

Fontes públicas sugeridas (verifique licença de uso):
- https://github.com/thiagobodruk/biblia (JSON em PT-BR)

---

## 🖥️ Criar atalho na Área de Trabalho

Crie um arquivo `Biblia ACF.bat` na Área de Trabalho:

```bat
@echo off
cd /d "C:\Caminho\Para\biblia_acf_windows"
python main.py
```

Ou, para não exibir o terminal, crie um `Biblia ACF.vbs`:

```vbs
Set oShell = CreateObject("WScript.Shell")
oShell.Run "python ""C:\Caminho\Para\biblia_acf_windows\main.py""", 0, False
```

---

## 📁 Estrutura do banco de dados

O arquivo `data/biblia.db` é criado automaticamente na primeira execução.  
Tabelas:

| Tabela | Conteúdo |
|---|---|
| `books` | 66 livros (nome, testamento, nº capítulos) |
| `reading_progress` | capítulos lidos por livro |
| `user_profile` | nome do usuário e tema |

---

## 📄 Licença

MIT — uso livre para fins pessoais e educacionais.