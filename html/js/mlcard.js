var cards = new Vue({
    el: '#cards',
    data: {
      tokumon_cards: [
        { 
          no: 1,
          identifier: 'pclass',
          name: 'チケットクラス',
        },
        { 
          no: 2,
          identifier: 'sex',
          name: 'せいべつ',
        },
        { 
          no: 3,
          identifier: 'age',
          name: 'ねんれい',
        },
        { 
          no: 4,
          identifier: 'sibsp',
          name: 'きょうだい・はいぐうしゃのかず',
        },
        { 
          no: 5,
          identifier: 'parch',
          name: 'おや・こどものかず',
        },
        { 
          no: 6,
          identifier: 'fare',
          name: 'りょうきん',
        },
        { 
          no: 7,
          identifier: 'embarked',
          name: 'しゅっぱつち',
        },
        { 
          no: 8,
          identifier: 'home.dest',
          name: 'もくてきち',
        },
        { 
          no: 9,
          identifier: 'cabin_head',
          name: 'へやばんごう♂',
        },
        { 
          no: 10,
          identifier: 'cabin_isodd',
          name: 'へやばんごう♀',
        },
        { 
          no: 11,
          identifier: 'name_honorific',
          name: 'けいしょう',
        },
        { 
          no: 12,
          identifier: 'boat',
          name: 'ボートばんごう',
        },
      ],
      selected_tokumon_cards: [],
      algorithm_cards: [
        {
          id: 1,
          name: 'ロジスティックかいき',
        },
        {
          id: 2,
          name: 'SVM',
        },
        {
          id: 3,
          name: 'ナイーブベイズ',
        },
        {
          id: 4,
          name: 'Kきんぼうほう',
        },
        {
          id: 5,
          name: 'けっていぎ',
        },
        {
          id: 6,
          name: 'ランダムフォレスト',
        },
        {
          id: 7,
          name: 'こうばいブースティング',
        },
        {
          id: 8,
          name: 'ニューラルネット',
        },
      ],
      selected_algorithm_card: null,
      score: null, 
    },
    methods: {
      selectTokumonCard : function(c){
        if (this.selected_tokumon_cards.includes(c)){
          this.selected_tokumon_cards = this.selected_tokumon_cards.filter(n => n !== c);
        }else{
          this.selected_tokumon_cards.push(c);
        }
      },
      tokumonImgCss : function(c){
        if (this.selected_tokumon_cards.includes(c)){
          return ['selected'];
        }else{
          return ['nonselect'];
        }
      },
      tokumonImgFile : function(c){
        return './img/tokumon' + c.no + '.png';
      },
      selectAlgorithmCard : function(c){
        this.selected_algorithm_card = c;
      },
      algorithmImgCss : function(c){
        if (this.selected_algorithm_card == c){
          return ['selected'];
        }else{
          return ['nonselect'];
        }
      },
      algorithmImgFile : function(c){
        return './img/algorithm' + c.id + '.png';
      },
      getCalcScore: function(){
        url = 'http://localhost:5000/calc?';
        url = url + "tokumon="  + this.selected_tokumon_cards.map(c => c.identifier);
        url = url + "&algorithm=" + this.selected_algorithm_card.id;

        console.log(url)
        axios
          //.get('https://tokumon.roudoujin.net/')
          .get(url)
          .then(response => (this.score = response.data));
      }
    },
  })
