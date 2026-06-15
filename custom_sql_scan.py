import ast
import json
import os

issues = []

class AdvancedSQLiScanner(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path
        # Danh sách các "Nguồn ô nhiễm" (Sources) - Nơi user nhập dữ liệu vào
        self.tainted_sources = ["request.args", "request.form", "request.json", "input", "params"]
        # Danh sách các biến bị "nhiễm độc" trong quá trình chạy code
        self.tainted_variables = set()
        # Các từ khóa SQL để nhận diện
        self.sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE"]

    def _is_sql(self, text):
        if not isinstance(text, str): return False
        return any(kw in text.upper() for kw in self.sql_keywords)

    def _add_issue(self, node, message):
        issues.append({
            "engineId": "advanced-python-sqli-taint",
            "ruleId": "SQLI_TAINTED",
            "primaryLocation": {
                "message": message,
                "filePath": self.file_path,
                "textRange": {"startLine": node.lineno}
            },
            "type": "VULNERABILITY",
            "severity": "CRITICAL"
        })

    def _get_source_name(self, node):
        """Hàm bổ trợ để chuyển đổi object AST thành chuỗi text của biến"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            base = self._get_source_name(node.value)
            return f"{base}.{node.attr}" if base else node.attr
        elif isinstance(node, ast.Subscript):
            return self._get_source_name(node.value)
        return None

    def visit_Assign(self, node):
        """BƯỚC 1: THEO VẾT BIẾN (Taint Tracking)
        Nếu một biến được gán bằng dữ liệu từ 'Source' độc hại, 
        hoặc gán bằng một biến đã bị nhiễm độc từ trước -> Đánh dấu nó bị nhiễm độc.
        """
        source_str = self._get_source_name(node.value)
        
        # Kiểm tra xem vế phải có phải là Source độc hại không (Ví dụ: request.args.get('id'))
        is_from_source = any(src in str(source_str) or (isinstance(node.value, ast.Call) and src in self._get_source_name(node.value.func)) 
                             for src in self.tainted_sources)

        # Hoặc vế phải là một biến đã bị nhiễm độc từ trước
        is_from_tainted_var = source_str in self.tainted_variables

        if is_from_source or is_from_tainted_var:
            for target in node.targets:
                var_name = self._get_source_name(target)
                if var_name:
                    self.tainted_variables.add(var_name) # Đóng dấu nhiễm độc biến này

        self.generic_visit(node)

    def visit_BinOp(self, node):
        """BƯỚC 2: PHÁT HIỆN ĐIỂM CHẾT (Sink)
        Nếu phát hiện phép cộng chuỗi (+) mà một vế là SQL, vế còn lại là biến bị nhiễm độc.
        """
        if isinstance(node.op, ast.Add):
            left_val = getattr(node.left, 'value', None)
            right_val = getattr(node.right, 'value', None)
            
            left_is_sql = self._is_sql(left_val)
            right_is_sql = self._is_sql(right_val)

            if left_is_sql:
                right_var = self._get_source_name(node.right)
                if right_var in self.tainted_variables:
                    self._add_issue(node, f"SQL Injection: Chuỗi SQL nối với biến nguy hiểm '{right_var}' lấy từ người dùng.")
            
            if right_is_sql:
                left_var = self._get_source_name(node.left)
                if left_var in self.tainted_variables:
                    self._add_issue(node, f"SQL Injection: Chuỗi SQL nối với biến nguy hiểm '{left_var}' lấy từ người dùng.")

        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        """BƯỚC 2.2: PHÁT HIỆN QUA F-STRING
        Nếu f-string chứa SQL và biến truyền vào nằm trong danh sách nhiễm độc.
        """
        has_sql = any(isinstance(v, ast.Constant) and self._is_sql(v.value) for v in node.values)
        if has_sql:
            for v in node.values:
                if isinstance(v, ast.FormattedValue):
                    var_name = self._get_source_name(v.value)
                    if var_name in self.tainted_variables:
                        self._add_issue(node, f"SQL Injection: f-string chứa SQL sử dụng biến nguy hiểm '{var_name}'.")

        self.generic_visit(node)

# --- Thực thi quét ---
current_script = os.path.basename(__file__)
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py") and file != current_script:
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=path)
                scanner = AdvancedSQLiScanner(path)
                scanner.visit(tree)
            except Exception:
                continue

with open("custom-issues.json", "w", encoding="utf-8") as f:
    json.dump({"issues": issues}, f, indent=4, ensure_ascii=False)
print(f"Quét xong. Tìm thấy {len(issues)} lỗi SQLi nguy hiểm thực sự.")