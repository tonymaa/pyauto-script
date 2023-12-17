class OperatorUtils:
    @staticmethod
    def operateJudgement(leftValue, rightValue, operator):
        if operator == ">":
            return leftValue > rightValue
        elif operator == "<":
            return leftValue < rightValue
        elif operator == "=":
            return leftValue == rightValue
        elif operator == ">=":
            return leftValue > rightValue and leftValue == rightValue
        elif operator == "<=":
            return leftValue < rightValue and leftValue == rightValue
        elif operator == "!=":
            return leftValue != rightValue