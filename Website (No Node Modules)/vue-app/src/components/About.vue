<template>
    <div>
        <b-card>
            <b-card-text>
                <h1>What is PoliCheck?</h1>
                <h5 class="text-secondary">
                    PoliCheck takes in news sites and uses a trained recurrent neural network to evaluate the bias of the article.<br/><br/>
                    To use the service, input a news article's URL into the searchbar and click "search." <br/><br/>
                    The website will take care of the restand provide you with a detailed evaluation of the article!
                </h5>
            </b-card-text>
        </b-card>
        <b-card>
            <b-card-text>
            <h1>How Does it Work?</h1>
                <h5 class="text-secondary">
                    Our neural network was trained with ~1200 articles deemed conservative or liberal. Information regarding the data<br> can be found <a href="https://arxiv.org/pdf/1904.01546.pdf">here</a>.<br/><br/>
                    Using this data, the neural network wrote two sample articles, one right-leaning and one left-leaning. These sample <br>
                    articles represent the entire data set as a whole.<br/>
                    <br/>
                    Whenever you input a URL, our website first scrapes the article from whatever page you inputted. It then compares that text to each corpus and computes how much the sentiments match
                    each of sample texts. Using this, we compute how biased the article is!
                </h5>
        </b-card-text>

        </b-card>
    </div>
</template>