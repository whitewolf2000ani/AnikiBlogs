---
title: ASTx to Python Mapping Strategy
date: 2025-03-24
---

---
## 1. Expression Node Mapping

### ASTx BinaryOp → Python ast.BinOp

**ASTx Structure**:

```python
BinaryOp(
    lhs: Expr,
    rhs: Expr,
    op: BinaryOpKind
)
```

**Python AST Equivalent**:

```python
ast.BinOp(
    left: ast.expr,
    op: operator,
    right: ast.expr
)
```

**Conversion Logic**:

```python
# Operator mapping table
OP_MAP = {
    BinaryOpKind.add: ast.Add(),
    BinaryOpKind.sub: ast.Sub(),
    BinaryOpKind.mul: ast.Mult()
}

@dispatch
def visit(self, node: BinaryOp) -> ast.BinOp:
    return ast.BinOp(
        left=self.visit(node.lhs),
        op=OP_MAP[node.op],
        right=self.visit(node.rhs)
    )
```


---

## 2. Statement Node Mapping

### ASTx DeleteStmt → Python ast.Delete

**ASTx Structure**:

```python
DeleteStmt(
    value: Iterable[Identifier]
)
```

**Python AST Equivalent**:

```python
ast.Delete(
    targets: list[ast.expr]
)
```

**Conversion Logic**:

```python
@dispatch
def visit(self, node: DeleteStmt) -> ast.Delete:
    return ast.Delete(
        targets=[ast.Name(id=ident.value, ctx=ast.Del()) 
                for ident in node.value]
    )
```

**Special Handling**:

- Convert ASTx Identifiers to Python Name nodes with Del context
- Handle nested deletion targets (e.g., del x)

---

## 3. Declaration Mapping

### ASTx VariableDeclaration → Python ast.Assign

**ASTx Structure**:

```python
VariableDeclaration(
    name: str,
    type_: DataType,
    value: Expr
)
```

**Python AST Equivalent**:

```python
ast.Assign(
    targets: list[ast.Name],
    value: ast.expr
)
```

**Conversion Logic**:

```python
@dispatch
def visit(self, node: VariableDeclaration) -> ast.Assign:
    return ast.Assign(
        targets=[ast.Name(id=node.name, ctx=ast.Store())],
        value=self.visit(node.value)
    )
```

**Edge Cases**:

- Support for multiple assignment targets

---

## 4. Control Flow Mapping

### ASTx IfStmt → Python ast.If

**ASTx Structure**:

```python
IfStmt(
    condition: Expr,
    then_block: list[Statement],
    else_block: list[Statement]
)
```

**Python AST Equivalent**:

```python
ast.If(
    test: ast.expr,
    body: list[ast.stmt],
    orelse: list[ast.stmt]
)
```

**Conversion Logic**:

```python
@dispatch
def visit(self, node: IfStmt) -> ast.If:
    return ast.If(
        test=self.visit(node.condition),
        body=[self.visit(stmt) for stmt in node.then_block],
        orelse=[self.visit(stmt) for stmt in node.else_block]
    )
```

**Special Handling**:

- Empty else block conversion
- Nested if-elif-else structures

---

## 5. Function Definition Mapping

### ASTx FunctionDef → Python ast.FunctionDef

**ASTx Structure**:

```python
FunctionDef(
    name: str,
    args: Arguments,
    return_type: DataType,
    body: list[Statement]
)
```

**Python AST Equivalent**:

```python
ast.FunctionDef(
    name: str,
    args: ast.arguments,
    body: list[ast.stmt],
    decorator_list: list[ast.expr]
)
```

**Conversion Logic**:

```python
@dispatch
def visit(self, node: FunctionDef) -> ast.FunctionDef:
    return ast.FunctionDef(
        name=node.name,
        args=self.visit(node.args),
        body=[self.visit(stmt) for stmt in node.body],
        decorator_list=[],
        returns=ast.Name(id=node.return_type.__name__)
    )
```

**Special Handling**:

- Argument type annotations
- Return type declarations
- Decorator support

---

## 6. Context Management Strategy

**ASTx Context**:

```python
Variable(
    name: str,
    type_: DataType
)
```

**Python Context Handling**:

```python
class ContextManager:
    def __init__(self):
        self.scope_stack = [{}]
    
    def add_variable(self, name: str, node: ast.AST):
        self.scope_stack[-1][name] = node
        
    def get_variable(self, name: str) -> ast.expr:
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable {name} not defined")
```

---

## Validation Strategy
- Round Trip Validation

```python
def test_binary_op_roundtrip():
    # ASTx → Python AST → Python code
    astx_node = BinaryOp(LiteralInt32(2), LiteralInt32(3), BinaryOpKind.add)
    transpiler = ASTxPythonASTTranspiler()
    py_ast = transpiler.visit(astx_node)
    
    # Generate Python code
    code = ast.unparse(py_ast)
    assert code == "(2 + 3)"
```


