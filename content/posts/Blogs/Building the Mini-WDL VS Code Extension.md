---
title: A VsCode extension for Mini-WDL
date: 2025-04-02
---

### **Introduction**

Creating a VS Code extension for Mini-WDL was an exciting journey filled with learning, debugging, and problem-solving. This blog details how I implemented syntax highlighting and language configuration for Mini-WDL, along with the challenges I faced—particularly around marking comments correctly—and how I overcame them. Let’s dive in!

---

### **1. Setting Up the Project**

#### **Step 1: Followed the documentation [VsCode](https://code.visualstudio.com/api/get-started/your-first-extension)

To start, I used Yeoman’s generator to create the basic structure of the VS Code extension:

```bash
mkdir mini-wdl-extension
cd mini-wdl-extension
npx yo code
```

During the prompts, I chose:

- **TypeScript** for type safety
- **No bundler** for simplicity
- **npm** as the package manager

This generated a project structure with files like `extension.ts`, `package.json`, and `.vscode/launch.json`.

- Folder Structure, we need to create a syntaxes directory mentioned.
``` JSON
mini-wdl-extension/
├── .vscode/                      # VS Code-specific settings
│   ├── launch.json               # Debug configuration for the extension
│   └── tasks.json                # Task runner configuration
├── src/                          # VS Code extension source files
│   ├── extension.ts              # Main entry point for the VS Code extension
│   ├── server.ts                 # Language client setup for connecting to the server
├── syntaxes/                     # TextMate grammar for syntax highlighting
│   └── mini-wdl.tmLanguage.json  # Syntax highlighting rules for Mini-WDL
├── language-configuration.json   # Language-specific editor configurations (e.g., comments, brackets)
├── package.json                  # VS Code extension metadata and dependencies
├── tsconfig.json                 # TypeScript configuration for the extension
├── README.md                     # Documentation for your extension (this file)
└── node_modules/                 # Node.js dependencies (created after `npm install`)

```

---

### **2. Adding Syntax Highlighting**

#### **Step 2: Creating TextMate Grammar**

I created a TextMate grammar file (`syntaxes/mini-wdl.tmLanguage.json`) to define syntax highlighting rules for WDL keywords, strings, and comments.

Here’s what the grammar looked like:

```json
{
  "name": "Mini WDL",
  "scopeName": "source.mini-wdl",
  "fileTypes": ["wdl"],
  "patterns": [
    { "include": "#keywords" },
    { "include": "#comments" },
    { "include": "#strings" }
  ],
  "repository": {
    "keywords": {
      "patterns": [
        {
          "name": "keyword.control.mini-wdl",
          "match": "\\b(task|workflow|input|output|command)\\b"
        }
      ]
    },
    "comments": {
      "patterns": [
        {
          "name": "comment.line.number-sign.mini-wdl",
          "match": "#.*$"
        }
      ]
    },
    "strings": {
      "patterns": [
        {
          "name": "string.quoted.double.mini-wdl",
          "begin": "\"",
          "end": "\"",
          "patterns": [
            {
              "name": "constant.character.escape.mini-wdl",
              "match": "\\\\."
            }
          ]
        }
      ]
    }
  }
}
```

---

### **3. Configuring Language Basics**

#### **Step 3: Language Configuration File**

I added a language configuration file (`language-configuration.json`) to define comment styles, brackets, and auto-closing pairs:

```json
{
  "comments": {
    "lineComment": "#"
  },
  "brackets": [
    ["{", "}"],
    ["[", "]"],
    ["(", ")"]
  ],
  "autoClosingPairs": [
    { "open": "{", "close": "}" },
    { "open": "[", "close": "]" },
    { "open": "\"", "close": "\"" },
    { "open": "'", "close": "'" }
  ]
}
```

This ensured that typing `{` or `"` would automatically close with `}` or `"`.

---

### **4. Challenges Faced**

#### **Problem: Comments Not Getting Marked Correctly and the keywords didn't highlight**

Initially, comments were not being detected or highlighted properly in `.wdl` files. This was frustrating because comments are critical for workflow readability.
![Image Description](https://whitewolf2000ani.github.io/AnikiBlogs/images/Screenshot_2025-04-06_131443_1.png)
*The comments, keywords were not hihglighted as you can see in this image.*

#### **Root Cause:**

The issue was with my regex pattern for comments in the TextMate grammar file. My initial implementation only matched simple `#` comments but failed when there were special characters or escaped sequences.

#### **Solution:**

I updated the regex to handle edge cases like escaped characters within comments:


```json
{
  "name": "comment.line.number-sign.mini-wdl",
  "match": "#.*$"
}
```

Update the `mini-wdl.tmLanguge.json` to make it more robust
```JSON
{
    "name": "Mini WDL",
    "scopeName": "source.mini-wdl",
    "fileTypes": ["wdl"], 
    "patterns": [
      { "include": "#keywords" },
      { "include": "#strings" },
      { "include": "#comments" },
      { "include": "#types" },
      { "include": "#variables" }
    ],
    "repository": {
      "keywords": {
        "patterns": [
          {
            "name": "keyword.control.mini-wdl",
            "match": "\\b(task|workflow|call|if|else|then|scatter|input|output|command|meta|parameter_meta|runtime)\\b"
          }
        ]
      },
      "strings": {
        "patterns": [
          {
            "name": "string.quoted.double.mini-wdl",
            "begin": "\"",
            "end": "\"",
            "patterns": [
              {
                "name": "constant.character.escape.mini-wdl",
                "match": "\\\\."
              }
            ]
          },
          {
            "name": "string.quoted.single.mini-wdl",
            "begin": "'",
            "end": "'",
            "patterns": [
              {
                "name": "constant.character.escape.mini-wdl",
                "match": "\\\\."
              }
            ]
          }
        ]
      },
      "comments": {
        "patterns": [
          {
            "name": "comment.line.number-sign",
            "match": "#.*$"
          }
        ]
      },
      "types": {
        "patterns": [
          {
            "name": "storage.type.mini-wdl",
            "match": "\\b(Boolean|Int|Float|String|File|Array|Map|Object|Pair)\\b"
          }
        ]
      },
      "variables": {
        "patterns": [
          {
            "name": "variable.other.mini-wdl",
            "match": "\\b[a-zA-Z][a-zA-Z0-9_]*\\b"
          }
        ]
      }
    }
  }
  
```
Additionally, I verified token scopes using VS Code’s Developer Tools: (==This helped me a lot==)

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS).
2. Type “Developer: Inspect Editor Tokens and Scopes.”
3. Click on different parts of your code to see applied tokens.

This helped me confirm that comments were now being marked correctly!
![Image Description](https://whitewolf2000ani.github.io/AnikiBlogs/images/Pasted_image_20250408112347.png)
*And then we got this* 😖😁 *everything came to light*

---

### **5. Testing the Extension**

#### **Step 4: Creating a Test File**

I created a test file (`test.wdl`) to verify syntax highlighting and language configuration:

```wdl
# This is a test WDL workflow
task hello {
  input {
    String name
    Int count = 3
  }
  command {
    echo "Hello ${name}"
    echo "Count: ${count}"
  }
}
workflow test_workflow {
  input {
    String person_name = "World"
  }
  call hello {
    input:
      name = person_name
  }
}
```


#### **Step 5: Running the Extension**

1. Compile the extension:

```bash
npm run compile
```

2. Launch in debug mode (or press F5 in VS Code).

When I opened `test.wdl`, keywords like `task`, `workflow`, and `input` were correctly highlighted, and comments were marked as expected.


---

### **6. Lessons Learned**

1. **Regex Debugging:** Writing robust regex patterns requires testing edge cases (e.g., escaped characters). Tools like VS Code’s scope inspector are invaluable.
2. **Language Configuration:** Small details like auto-closing pairs significantly improve usability.
3. **Testing Matters:** Creating test files early helps catch issues before they become blockers.

---

### **7. Conclusion**

Building this Mini-WDL extension taught me how language tooling works under the hood—from defining syntax rules to debugging token scopes. While solving issues like comment detection was challenging, it reinforced my understanding of TextMate grammars and VS Code’s API.
This project is just the beginning! With basic syntax highlighting and language configuration in place, I’m excited to explore advanced features like semantic highlighting and LSP integration in the next blog.
A blog on working with WDL is also coming up!
If you’re interested in building your own extensions or contributing to WDL tooling, check out my GitHub repository: [github.com/whitewolf2000ani/Mini-WDL](https://github.com/whitewolf2000ani/Mini-WDL).

