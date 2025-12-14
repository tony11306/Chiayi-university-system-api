class Semester:
    def __init__(self, year: int, term: int):
        self.year = year
        self.term = term

    def __repr__(self):
        return f"{self.year} 學年度 第 {self.term} 學期"