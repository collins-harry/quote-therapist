const BaseLocalGame = require('./../BaseLocalGame');

const config = require('./gameConfig');
const copy   = require('./copy');

const fs = require('fs');
const request = require('request');
const path = require('path');

// Do not change this, this is to seperate the scripts of the participating teams
const teamname = path.dirname(__filename).split(path.sep).pop();


class HackathonGame extends BaseLocalGame {
    /**
     *
     * @param {function} requestCallback
     * @param {string} language
     * @param {boolean} skipIntro
     */
    constructor(requestCallback, language, skipIntro){
        super(requestCallback, language, skipIntro);

        this.finalStep = 9;
        this.currentInteractionStep = this.skipIntro? 2 : 0;

        this.currentImageExecId = null;
        this.currentVoiceExecId = null;
        this.currentGestureExecId = null;
        this.currentImageOutput = null;
        this.currentGestureInput = null;
        this.sentences = copy.getSentences(this.language);
		
		//this.guessedCountry = "unknown"
		//this.picture = "unknown"
		
        this.randomProcessingTimeout = null;
        this.processingLoop = 0;
        this.forceDone = false;
		
      
    }

    start(){
        console.log("game from Hakkende Rakkers has started! :)");
        this._say("Hanlo mijn jongen, met hond is waar u mee spreekt", false, true);
        this._nextStep();
    }
    pause(){
        super.pause();
    }
    continue(){
        super.continue();
        switch(this.currentInteractionStep){
            // do something according to where it was
            // e.g. repeat current step (so this.currentInteractionStep--)
            case 3:
            case 4:
            case 5:
                // reset countdown
                this.currentInteractionStep = 4;
                break;
            case 6:
            case 7:
            case 8:
                // do nothing
                break;
            default:
                this.currentInteractionStep--;
                break;
        }
        this._nextStep();
    }
    stop(){
        super.stop();
    }


    goToNextStep(){
        // this.currentInteractionStep++;
        // this._nextStep();
    }

    goToFirstStep(){
        this.currentInteractionStep = 0;
        this._nextStep();
    }

    goToNextStep2(){
        this.currentInteractionStep++;
        this._nextStep();
    }

    _nextStep(){
        console.log("nextStep entered");
        if(!this.paused){
            console.log("nextStep: currentInteractionStep "+this.currentInteractionStep);
            switch(this.currentInteractionStep){
                case 0:
                    this._say("Wij gaan hopelijk opnemen strakjes", false)
                    this._handleRecord()
                    break;
                case 1:
                    this._say("HANLO wij hebben input gekregen, heel mooi.", false);
                    this.goToFirstStep();
                    break;
                // case 2:
                //     // explain how to trigger camera and what to do with the item
                //     this._say(this.sentences.AskInput, true);
                //     break;
                // case 3:
                //     // retrieve image
                //     setTimeout(() => {
                //         this._getImage();
                //         this.goToNextStep();
                //     }, 1000);
                //     break;
                // case 4:
				
                //     // send image to google vision api and tell user you are processing
                //     this._say(this.sentences.RespondStartProcessing, true, true);

                //     this.randomProcessingTimeout = setTimeout(() => {
                //         this.processingLoop++;
                //         if(this.currentImageOutput) {
                //             this.goToNextStep();

                //         } else if(this.processingLoop > config.MAX_PROCESSING_LOOP) {
                //             // kill for unknown --> next step does this already
                //             this.goToNextStep();
                //         } else {
                //             //this.say(this.sentences.RandomProcessing.normal, true, true);
                //             this._nextStep();
                //         }
                //     }, config.PROCESSING_TIMEOUT_TIME);
                //     break;
					
                // case 5:
					
                //     // output to person the data you think you have
                //     // done via handleCameraInput             

				// 	if(this.currentImageOutput) {					
						
				// 		var sentence = this.currentImageOutput.message;							
				// 		this._say(sentence, false, true);
						
				// 	}else{
						
				// 		this._say(this.sentences.AnswerDontKnow);
				// 		this.forceDone = true;		
				// 		this.goToNextStep();
						
				// 	}
					
	            //     break; 
					
                // case 6:
                //     // ask person if you are correct
                //     this._say(this.sentences.AskCorrect, true);
                //     break;
                // case 7:
                //     // wait for person response if you are correct
                //     this._setInputListener();
                //     this._say(this.sentences.AskGestureHint[0], false, true);
                //     break;
                // case 8:
                //     // give proper reaction to correct or not. trigger parent event and end the game
                //     if(this.currentGestureInput === "gesture|thumb_up") {
                //         this._say(this.sentences.AnswerCorrect, true);
                //     } else { 
                //         this._say(this.sentences.AnswerWrong.normal, true);                        
                //     }
                //     break;
                case 2:
                    // game ended
                    this._say("HANLO MET HOND This is the end", false)
                    this.request(this.actions.DONE);
                    break;
                default:
                    // oops, something went wrong....
                    this.forceDone = true;
                    this._say(["Oops, something went wrong."]);
                    break;
            }
        }
    }


    /**
     *
     * @param {string|array} sentences
     * @param {boolean} [isRandom]
     * @param {boolean} [blockNextStep]
     *
     */
    _say(sentences, isRandom, blockNextStep){
        const sentence = isRandom? this.constructor.pickRandomSentence(sentences) : sentences;
        const eventOutputObject = this.request(this.actions.VOICE, this.methods.Voice.SAY, sentence);

        if(!blockNextStep) this.currentVoiceExecId = eventOutputObject.data.execId;
    }

    _handleRecord(){
		
		var _this = this;
        
        var url = "http://127.0.0.1:5555/api/" + teamname + "/janschut"
        var req = request.post(url, function (err, resp, body) {
            if (err) {
                console.log("Game | " + teamname + " | request.post() | handleRecord | error", err);
                _this.forceDone = true;
                _this._say("Sorry, I don't know now", true);
            } else {
                console.log('URL: ' + body);
                var pars = JSON.parse(body);
                console.log('HANLO MET HOND response:' + pars.message);
                clearTimeout(this.randomProcessingTimeout);
                _this.goToNextStep2();
            }
        });
    }





    _getImage(){
        const eventObj = this.request(this.actions.CAMERA,this.methods.Camera.GET_IMAGE);
        this.currentImageExecId = eventObj.data.execId;
    }

    _setInputListener(){
        const eventObj = this.request(this.actions.INPUT, this.methods.Input.START_LISTENING, {
            inputs: ['gesture|thumb_up', 'gesture|thumb_down'],
            timeoutTime: 10000,
            help: true,
            helpSentence: this.sentences.AskGestureHint[0]
        });
        this.currentGestureExecId = eventObj.data.execId;
    }

    handle(obj){
        const {data: result, execId, action} = obj;		
        switch(action){
            case this.actions.CAMERA:				
                this._handleCameraInput(execId, result.image);
                break;
            case this.actions.VOICE:
                this._handleVoiceOutput(execId);
                break;
            case this.actions.INPUT:
                this._handleGestureInput(execId, result);
                break
        }
    }

    _handleCameraInput(execId, base64_image){
		
		var _this = this;
        if(execId === this.currentImageExecId) {
            // store the image somehow
			
            const base64Data = base64_image//.replace(/^data:image\/png;base64,/, "");
            const path = __dirname + '/image-cache.png';		

            fs.writeFile(path, base64Data, 'base64', err => {
				
                if(!err){
					
					var url = "http://127.0.0.1:5555/api/" + teamname + "/route01"
					var req = request.post(url, function (err, resp, body) {
						if (err) {
							console.log("Game | " + teamname + " | request.post() | error", err);
							_this.forceDone = true;
							_this._say("Sorry, I don't know now", true);
						} else {
							console.log('URL: ' + body);
							_this.currentImageOutput = JSON.parse(body);
							clearTimeout(this.randomProcessingTimeout);
							_this.goToNextStep();
						}
					});
					var form = req.form();
					form.append('photo', fs.createReadStream(path));					
					
                } else {
                    console.log("Game | " + teamname + " | writeFile() | error", err);
                    this.forceDone = true;
                    this._say("Sorry, I don't know now", true);
                }
            });
        } else {
            // todo some error stuff
			
        }
    }


    /**
     *
     * @param {number} execId
     */
    _handleVoiceOutput(execId) {
        if(execId === this.currentVoiceExecId) {
            setTimeout(() => {
                if(this.forceDone) {
                    this.currentInteractionStep = this.finalStep;
                    this._nextStep();
                }
                else this.goToNextStep();
            }, 200);
        }
    }

    /**
     *
     * @param {number} execId
     * @param {object} result
     * @private
     */
    _handleGestureInput(execId, result){
        if(execId === this.currentGestureExecId ) { // --> && success cause the error, cuz not always success
            // console.log("app | handleGestureInput() | data:");
            // console.dir(result, {colors:true, depth: 5});

            const { triggered } = result;
            this.currentGestureInput = triggered;
            this.goToNextStep();
        }
    }


    /**
     *
     * @param {string[]} sentences
     * @returns {string}
     */
    static pickRandomSentence(sentences) {
        return sentences[Math.floor(Math.random() * sentences.length)];
    }

    /**
     *
     * @param {string} sentence
     * @param {string} guess
     * @returns {string}
     */
    static buildGuessSentence(sentence, guess) {
        const isVowel = ['a','e','i','o','u'].indexOf(guess.charAt(0).toLowerCase()) > -1 ;

        const prefix = isVowel ? 'an ' : 'a ';

        return sentence.replace(/\[result]/g, prefix+guess);
    }

    //_________________________________________________________________________________________________________________/

    /**
     *
     * @returns {string}
     * @constructor
     */
    static get Name(){
        return teamname;
    }

    /**
     *
     * @returns {config.GameChoices|number}
     * @constructor
     */
    static get Category(){
        return 2;
    }

    /**
     *
     * @returns {string}
     * @constructor
     */
    static get Description(){
        return 'Example description for ' + teamname;
    }

    /**
     *
     * @returns {boolean}
     * @constructor
     */
    static get NeedsInternet(){
        return true;
    }
}
module.exports = HackathonGame;