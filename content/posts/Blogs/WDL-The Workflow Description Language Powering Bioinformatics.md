---
title: What I learned about WDL
date: 2025-03-28
---
---

### **What is WDL?**

The **Workflow Description Language (WDL)** is an open-source language designed to simplify complex computational workflows, particularly in genomics and bioinformatics. Developed by the Broad Institute and maintained by the OpenWDL community, WDL allows scientists to define analysis pipelines in a human-readable format.

**Why It Matters**:

- Standardizes workflow definitions across platforms
- Enables reproducibility in scientific research
- Simplifies scaling from laptops to cloud environments

---

### **WDL Syntax: A Step-by-Step Breakdown**

Let’s dissect a simple WDL workflow to understand its structure.
#### **Example Workflow**

```wdl
version 1.2  # Modern WDL version

task say_hello {
    input {
        String greeting
        String name
    }
    
    command <<<;
        echo "~{greeting}, ~{name}!"
    >>>;
    
    output {
        String message = read_string(stdout())
    }
    
    requirements {
        container: "ubuntu:latest"
    }
}

workflow main {
    input {
        String name
        Boolean is_pirate = false
    }
    
    Array[String] greetings = select_all([
        "Hello",
        "Hallo",
        "Hej",
        (
            if is_pirate
            then "Ahoy"
            else None
        ),
    ])
    
    scatter (greeting in greetings) {
        call say_hello {
            input:
                greeting = greeting,
                name = name
        }
    }
    
    output {
        Array[String] messages = say_hello.message
    }
}
```

---

### **Line-by-Line Breakdown**

#### **1. Version Declaration**

```wdl  
version 1.2  
```

- **New in 1.2**: Adds features like `select_all()` and improved error handling.
- **Best Practice**: Always declare versions explicitly for compatibility.

---

#### **2. Task Definition**

```wdl  
task say_hello {
  input {
      String greeting
      String name
  }
```

- **Input Parameters**: Declares two required inputs for personalization.
- **Flexibility**: Tasks can be reused across workflows with different inputs.

---

#### **3. Command Section (Heredoc Syntax)**

```wdl  
command >>>;
    echo "~{greeting}, ~{name}!"
<<<;  
```

- **`<<<;` Syntax**: Allows multi-line commands without escaping quotes.
- **Variable Substitution**: `~{}` injects WDL variables into shell commands.

---

#### **4. Output Declaration**

```wdl  
output {
    String message = read_string(stdout())
}
```

- **`read_string()`**: Built-in function captures command output.
- **Type Safety**: Explicit `String` type ensures data consistency.

---

#### **5. Runtime Requirements**

```wdl  
requirements {
    container: "ubuntu:latest"
}
```

- **Reproducibility**: Uses Docker containers for consistent environments.
- **Alternatives**: Can specify CPU/memory constraints instead.

---

#### **6. Workflow Inputs**

```wdl  
input {
    String name
    Boolean is_pirate = false
}
```

- **Default Values**: `is_pirate` is optional (defaults to `false`).
- **Runtime Flexibility**: Users can override defaults when executing.

---

#### **7. Array with Conditional Logic**

```wdl  
Array[String] greetings = select_all([
    "Hello",
    "Hallo",
    "Hej",
    (if is_pirate then "Ahoy" else None),
])
```

- **`select_all()`**: Filters out `None` values, creating a clean array.
- **Conditional Expression**: Adds "Ahoy" only if `is_pirate` is `true`.

---

#### **8. Parallel Execution**

```wdl  
scatter (greeting in greetings) {
    call say_hello { input: greeting, name }
}
```

- **Scatter/Gather**: Runs `say_hello` in parallel for each greeting.
- **Cloud Optimization**: Automatically scales on distributed systems.

---

#### **9. Workflow Output**

```wdl  
output {
    Array[String] messages = say_hello.message
}
```

- **Aggregation**: Collects outputs from all parallel tasks.
- **Downstream Use**: These messages could feed into another workflow.

---

### **Key WDL 1.2 Features Demonstrated**

1. **Conditional Arrays**:

```wdl  
(if is_pirate then "Ahoy" else None)
```

    - Enables dynamic workflow configurations based on inputs.
2. **Scatter Parallelization**:

```wdl  
scatter (greeting in greetings) { ... }
```

    - Simplifies parallel processing of large datasets.
3. **Type-Safe Outputs**:

```wdl  
Array[String] messages = say_hello.message
```

    - Ensures data integrity between workflow steps.

---

### **Running the Workflow**

**Input JSON**:

```json  
{
  "main.name": "Dave",
  "main.is_pirate": true
}
```

**Expected Output**:

```json  
{
  "main.messages": ["Hello, Dave!", "Hallo, Dave!", "Hej, Dave!", "Ahoy, Dave!"]
}
```

---

### **Getting Started with WDL**

1. **Install a WDL Runner**:

```bash  
# For MiniWDL (used in our project):  
pip install miniwdl  
```

2. **Write Your First Workflow**:

```wdl  
version 1.0  
workflow hello_wdl {  
  call say_hello  
  output {  
    String message = "Workflow completed!"  
  }  
}  
task say_hello {  
  command { echo "Hello, WDL!" }  
}  
```

3. **Run It**:

```bash  
miniwdl run hello.wdl  
```


---

### **Conclusion**

By learning WDL, I gained the foundation needed to build tools around WDL, which aims to make workflow development even more intuitive.

**Resources**:

- [OpenWDL Documentation](https://docs.openwdl.org/) -> The documentation is really good to understand WDL.
- [WDL Quickstart Guide](https://docs.openwdl.org/getting-started/quickstart.html)


