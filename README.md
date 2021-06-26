# MOZE_Analysis
+ ```MOZE```是一套手機記帳軟體APP，詳情請見[官方網站](https://moze.app/)  
+ APP裡面已經提供了非常好用的使用者介面，可以很簡單的分析消費，但有一些比較複雜的分析可能是APP裡面做不太到的  
+ APP作者也提供匯出功能，可以將個人的資料以csv檔案([匯出格式](https://doc.moze.app/feature/import-export#export))匯出做後續分析  
+ 本專案將csv的資料轉換成三大類別整理成結構化的型態，可以比較方便用一些繪圖package做分析(當然你也可以直接透過```pandas```操作csv做分析)  

# Requirements
+ joblib
+ pandas
+ plotly

# 使用方式
1. 將匯出的檔案命名為```MOZE.csv```(應該也是```MOZE```APP預設名稱)
2. 把檔案放到此專案資料夾內
3. 執行```python extract.py -d all```，arguments詳細格式請參考[此章節](https://github.com/Huang-Jim/MOZE_Analysis/blob/main/README.md#extractpy)
4. 透過```joblib.load(month_sheets.pkl)```後，就能如同```structure_examples.ipynb```或是```plot_examples.ipynb```裡面提到的範例來分析資料了~

# extract.py
+ ```extract.py```會依照給定的期間(-d或--duration)將csv檔轉換成```month_sheets.pkl```
+ ```-d all``` : 將csv檔案的所有消費資料全部轉換為pkl檔
+ ```-d 年/月``` : 只轉換csv檔案內特定的某個年/月的消費資料
  + e.g. ```python extract.py -d 2021/5``` 代表將2021年5月的消費資料轉換成pkl檔
+ ```-d 年/月-``` : 轉換csv檔案內特定的某個年/月開始一直到最新的消費資料
  + e.g. ```python extract.py -d 2021/4-``` 代表將2021年4月開始一直到最新的年月的消費資料轉換成pkl檔
+ ```-d 年/月-年/月``` : 轉換csv檔案內特定的某個年/月開始一直到指定的年/月的消費資料
  + e.g. ```python extract.py -d 2020/4-2021/5``` 代表將2020年4月開始一直到2021年5月的消費資料轉換成pkl檔

# 三個資料型態
由大而小分別為```MonthSheet```、```MainItem```以及```SubItem```，詳情可以參考```structure_examples.ipynb```，裡面描述了類別內方便的調用方法

# 資料分析與做圖
將```MOZE.csv```轉換成```month_sheets.pkl```後，可以用簡單的程式將消費習慣量化，也可以透過如```matplotlib```或是```plotly```做視覺化呈現，本專案也提供一些與```plotly```互動的流程，詳情請參考```plot_examples.ipynb```
