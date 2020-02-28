Vue.component('player', {
  props: ['playerno'],
  data: function () {
    return {
      tokumon_cards: [
        { 
          no: 1,
          identifier: 'pclass',
          name: 'チケットクラス',
          is_dummy: true,
          is_na : false,
        },
        { 
          no: 2,
          identifier: 'sex',
          name: 'せいべつ',
          is_dummy: true,
          is_na : false,
        },
        { 
          no: 3,
          identifier: 'age',
          name: 'ねんれい',
          is_dummy: false,
          is_na : true,
        },
        { 
          no: 4,
          identifier: 'sibsp',
          name: 'きょうだい・はいぐうしゃのかず',
          is_dummy: false,
          is_na : false,
        },
        { 
          no: 5,
          identifier: 'parch',
          name: 'おや・こどものかず',
          is_dummy: false,
          is_na : false,
        },
        { 
          no: 6,
          identifier: 'fare',
          name: 'りょうきん',
          is_dummy: false,
          is_na : true,
        },
        { 
          no: 7,
          identifier: 'embarked',
          name: 'しゅっぱつち',
          is_dummy: true,
          is_na : true,
        },
        { 
          no: 8,
          identifier: 'home.dest',
          name: 'もくてきち',
          is_dummy: true,
          is_na : true,
        },
        { 
          no: 9,
          identifier: 'cabin_head',
          name: 'へやばんごう♂',
          is_dummy: true,
          is_na : true,
        },
        { 
          no: 10,
          identifier: 'cabin_isodd',
          name: 'へやばんごう♀',
          is_dummy: true,
          is_na : true,
        },
        { 
          no: 11,
          identifier: 'name_honorific',
          name: 'けいしょう',
          is_dummy: true,
          is_na : false,
        },
        { 
          no: 12,
          identifier: 'boat',
          name: 'ボートばんごう',
          is_dummy: true,
          is_na : true,
        },
      ],
      selected_tokumon_cards: [],
      selected_dummy_cards: [],
      selected_fillna_cards: [],
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
      recent_select_card: null,
      score: null, 
      isLoading: false,
      result_selected_tokumon_cards: [],
      result_selected_dummy_cards: [],
      result_selected_fillna_cards: [],
      result_selected_algorithm_card: null,
    }
  },
  methods: {
    selectTokumonCard : function(c){
      if (this.selected_tokumon_cards.includes(c)){
        this.selected_tokumon_cards = this.selected_tokumon_cards.filter(n => n !== c);
        this.selected_dummy_cards = this.selected_dummy_cards.filter(n => n !== c);
        this.selected_fillna_cards = this.selected_fillna_cards.filter(n => n !== c);
        this.recent_select_card = null;
      }else{
        this.selected_tokumon_cards.push(c);
        this.recent_select_card = c;
      }
    },
    selectDummyCard : function(c){
      if (this.selected_dummy_cards.includes(c)){
        this.selected_dummy_cards = this.selected_dummy_cards.filter(n => n !== c);
      }else{
        this.selected_dummy_cards.push(c);
      }        
    },
    selectFillNACard : function(c){
      if (this.selected_fillna_cards.includes(c)){
        this.selected_fillna_cards = this.selected_fillna_cards.filter(n => n !== c);
      }else{
        this.selected_fillna_cards.push(c);
      }      
    },
    tokumonImgCss : function(c){
      if (this.selected_tokumon_cards.includes(c)){
        return ['selected'];
      }else{
        return ['nonselect'];
      }
    },
    dummyImgCss : function(c){
      if (this.selected_dummy_cards.includes(c)){
        return ['dummy_selected'];
      }else if(this.recent_select_card == c && c.is_dummy){
        return ['dummy_nonselect'];
      }else{
        return ['dummy_none'];
      }
    },
    fillNAImgCss : function(c){
      if (this.selected_fillna_cards.includes(c)){
        return ['fillna_selected'];
      }else if(this.recent_select_card == c && c.is_na){
        return ['fillna_nonselect'];
      }else{
        return ['fillna_none'];
      }
    },
    tokumonCardImgStyle: function(c){
      return "top: " + (c.no-1)*90 + "px;";
    },
    tokumonImgFile : function(c){
      return './img/tokumon' + c.no + '.png';
    },
    algorithmCardImgStyle: function(c){
      return "top: " + (c.id-1)*45 + "px;";
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
      if(window.location.host==""){
        url = 'http://localhost:5000/calc?';
      }else{
        url = 'https://tokumon.roudoujin.net/calc?';
      }
      url = url + "tokumon="  + this.selected_tokumon_cards.map(c => c.identifier);
      url = url + "&dummy="  + this.selected_dummy_cards.map(c => c.identifier);
      url = url + "&fillna="  + this.selected_fillna_cards.map(c => c.identifier);
      url = url + "&algorithm=" + this.selected_algorithm_card.id;
      this.score = null;
      this.isLoading = true;
      this.result_selected_tokumon_cards = this.selected_tokumon_cards;
      this.result_selected_dummy_cards = this.selected_dummy_cards;
      this.result_selected_fillna_cards = this.selected_fillna_cards;
      this.result_selected_algorithm_card = this.selected_algorithm_card;
      console.log(url)
      axios
        .get(url)
        .then(response => {
            this.score = response.data;
            this.isLoading = false;
        });
    },
    getTokumonList : function(c){
      var result = c.name;

      if(this.result_selected_dummy_cards.includes(c)){
        result = result + "＋ダミーへんすうか"
      }

      if(this.result_selected_fillna_cards.includes(c)){
        result = result + "＋けっそんちほかん"
      }

      return result;

    },
  },
  computed: {
    isButtonDisable : function(){
      if(this.selected_algorithm_card != null &&
         this.selected_tokumon_cards.length >= 1 &&
         !this.isLoading){
        return false;
      }else{
        return true;
      }
    },
    isButtonVariant : function(){
      if(this.selected_algorithm_card != null &&
         this.selected_tokumon_cards.length >= 1 &&
         !this.isLoading){
        return 'danger';
      }else{
        return 'secondary';
      }
    },
    hasScore : function(){
      return (this.score!=null);
    },
    getAccuracy : function(){
      if(this.score!=null){
        return this.score['accuracy'];
      }else{
        return '';
      }
    },
    getResultAlgolithmName : function(){
      if(this.result_selected_algorithm_card != null){
        return this.result_selected_algorithm_card.name;
      }else{
        return; 
      }
    },
  },
  template: '#card-component',
})

var players = new Vue({
  el: '#players',
});
