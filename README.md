# MOZE_Analysis
```MOZE```是一套手機記帳軟體APP，詳情請見[官方網站](https://moze.app/)  
APP裡面已經提供了非常好用的使用者介面，可以很簡單的分析消費，但有一些比較複雜的分析可能是APP裡面做不太到的  
APP作者也提供匯出功能，可以將個人的資料以csv檔案([匯出格式](https://doc.moze.app/feature/import-export#export))匯出做後續分析  
本專案將csv的資料轉換成三大類別整理成結構化的型態，可以比較方便用一些繪圖package做分析(當然你也可以直接透過```pandas```操作csv做分析)  

# 三個資料型態
由大而小分別為```MonthSheet```、```MainItem```以及```SubItem```，詳情可以參考```structure_examples.ipynb```，裡面描述了類別內方便的調用方法

# 資料分析與做圖
將```MOZE.csv```轉換成```month_sheets.pkl```後，可以用簡單的程式將消費習慣量化，也可以透過如```matplotlib```或是```plotly```做視覺化呈現，本專案也提供一些與```plotly```互動的流程，詳情請參考```plot_examples.ipynb```
