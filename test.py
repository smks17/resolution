import json

import resolution

data = {}

with open("data.json") as file:
    data = json.load(file)
    
class TestClassResolution:
    def run_input_output(self, suffix):
        testNum = f'test{suffix}'
        testData = data[testNum]
        actual = resolution.prove(testData["premises"], testData["conclude"])
        expect = (testData["isProvable"], eval(testData["result"]))
        assert (actual[0] == expect[0]), "Provable is not same!"
        assert (actual[1].sort() == expect[1].sort()), "Prove set is not same!"
    
    def test_input01(self): self.run_input_output('1')
    def test_input02(self): self.run_input_output('2')
    def test_input03(self): self.run_input_output('3')
    def test_input04(self): self.run_input_output('4')
    def test_input05(self): self.run_input_output('5')
    def test_input06(self): self.run_input_output('6')
    def test_input07(self): self.run_input_output('7')
    def test_input08(self): self.run_input_output('8')
    def test_input09(self): self.run_input_output('9')
    def test_input10(self): self.run_input_output('10')
