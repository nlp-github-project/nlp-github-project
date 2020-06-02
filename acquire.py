"""
A module for obtaining repo readme and language data from the github API.

Before using this module, read through it, and follow the instructions marked
TODO.

After doing so, run it like this:

    python acquire.py

To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#        You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.


REPOS = [
       'freeCodeCamp/freeCodeCamp', '996icu/996.ICU', 'vuejs/vue',
       'EbookFoundation/free-programming-books', 'facebook/react',
       'tensorflow/tensorflow', 'twbs/bootstrap', 'sindresorhus/awesome',
       'getify/You-Dont-Know-JS', 'jwasham/coding-interview-university',
       'ohmyzsh/ohmyzsh', 'kamranahmedse/developer-roadmap',
       'github/gitignore', 'CyC2018/CS-Notes',
       'donnemartin/system-design-primer', 'microsoft/vscode',
       'airbnb/javascript', 'flutter/flutter', 'd3/d3', 'torvalds/linux',
       'facebook/react-native', 'jackfrued/Python-100-Days',
       'public-apis/public-apis', 'electron/electron',
       'vinta/awesome-python', 'Snailclimb/JavaGuide',
       'facebook/create-react-app', 'jlevy/the-art-of-command-line',
       'TheAlgorithms/Python', 'danistefanovic/build-your-own-x',
       'axios/axios', 'golang/go', 'trekhleb/javascript-algorithms',
       'nodejs/node', 'justjavac/free-programming-books-zh_CN',
       'ytdl-org/youtube-dl', 'animate-css/animate.css',
       'kubernetes/kubernetes', 'tensorflow/models', 'microsoft/terminal',
       'iluwatar/java-design-patterns', 'mui-org/material-ui',
       'moby/moby', '30-seconds/30-seconds-of-code',
       'PanJiaChen/vue-element-admin', 'MisterBooo/LeetCodeAnimation',
       'avelino/awesome-go', 'vuejs/awesome-vue', 'webpack/webpack',
       'jquery/jquery', 'spring-projects/spring-boot',
       'Semantic-Org/Semantic-UI', 'tonsky/FiraCode',
       'typicode/json-server', 'netdata/netdata', 'jakubroztocil/httpie',
       'rails/rails', 'xingshaocheng/architect-awesome',
       'goldbergyoni/nodebestpractices', 'ElemeFE/element',
       'h5bp/html5-boilerplate', 'opencv/opencv', 'lodash/lodash',
       'awesome-selfhosted/awesome-selfhosted',
       'josephmisiti/awesome-machine-learning', 'kdn251/interviews',
       'gatsbyjs/gatsby', 'h5bp/Front-end-Developer-Interview-Questions',
       'gohugoio/hugo', 'moment/moment', 'doocs/advanced-java',
       'bitcoin/bitcoin', 'ansible/ansible', 'antirez/redis',
       'yangshun/tech-interview-handbook', 'ReactiveX/RxJava',
       'labuladong/fucking-algorithm', 'nvm-sh/nvm',
       'resume/resume.github.com', 'ionic-team/ionic',
       'scikit-learn/scikit-learn', 'papers-we-love/papers-we-love',
       'ReactTraining/react-router', 'thedaviddias/Front-End-Checklist',
       'jekyll/jekyll', 'google/material-design-icons', 'jgthms/bulma',
       'awesomedata/awesome-public-datasets', 'pytorch/pytorch',
       'psf/requests', 'gothinkster/realworld',
       'protocolbuffers/protobuf', 'meteor/meteor',
       'mtdvio/every-programmer-should-know', 'kelseyhightower/nocode',
       'apache/incubator-echarts', 'necolas/normalize.css',
       'gin-gonic/gin', 'yarnpkg/yarn',
       'scutan90/DeepLearning-500-questions',
       'wasabeef/awesome-android-ui', 'jaywcjlove/awesome-mac',
       'NARKOZ/hacker-scripts', 'Dogfalo/materialize', 'google/guava',
       'aymericdamien/TensorFlow-Examples',
       'spring-projects/spring-framework',
       'minimaxir/big-list-of-naughty-strings', 'scrapy/scrapy',
       'Hack-with-Github/Awesome-Hacking', 'square/okhttp',
       'enaqx/awesome-react', 'neovim/neovim', 'nwjs/nw.js',
       'FreeCodeCampChina/freecodecamp.cn', 'babel/babel',
       'prettier/prettier', 'android/architecture-samples',
       'fatedier/frp', 'ryanmcdermott/clean-code-javascript',
       'serverless/serverless', 'sindresorhus/awesome-nodejs',
       'parcel-bundler/parcel', 'square/retrofit', 'impress/impress.js',
       'juliangarnier/anime', 'ripienaar/free-for-dev', 'grafana/grafana',
       'macrozheng/mall', 'nodejs/node-v0.x-archive', 'x64dbg/x64dbg',
       'ziishaned/learn-regex', 'vsouza/awesome-ios',
       'astaxie/build-web-application-with-golang', 'ColorlibHQ/AdminLTE',
       'tesseract-ocr/tesseract', 'gogs/gogs',
       'ageitgey/face_recognition',
       'MaximAbramchuck/awesome-interview-questions', 'sveltejs/svelte',
       'TryGhost/Ghost', 'k88hudson/git-flight-rules',
       'Alamofire/Alamofire', 'home-assistant/core',
       'prakhar1989/awesome-courses', 'vercel/hyper',
       'bailicangdu/vue2-elm', 'soimort/you-get',
       'tuvtran/project-based-learning', 'azl397985856/leetcode',
       'AFNetworking/AFNetworking', 'git/git', 'syncthing/syncthing',
       'adobe/brackets', 'Genymobile/scrcpy', 'etcd-io/etcd',
       'facebook/jest', 'prometheus/prometheus', 'karan/Projects',
       'mozilla/pdf.js', 'PhilJay/MPAndroidChart', 'discourse/discourse',
       'google/material-design-lite', 'justjavac/awesome-wechat-weapp',
       'python/cpython', 'godotengine/godot', '521xueweihan/HelloGitHub',
       'blueimp/jQuery-File-Upload', 'deepfakes/faceswap', 'hexojs/hexo',
       'BVLC/caffe', 'mermaid-js/mermaid', 'xitu/gold-miner',
       'preactjs/preact', 'grpc/grpc', 'open-guides/og-aws',
       'floodsung/Deep-Learning-Papers-Reading-Roadmap', 'apache/spark',
       'alex/what-happens-when', 'binhnguyennus/awesome-scalability',
       'ethereum/go-ethereum', 'Kong/kong',
       'kamranahmedse/design-patterns-for-humans',
       'DefinitelyTyped/DefinitelyTyped', 'Solido/awesome-flutter',
       'huggingface/transformers', 'Leaflet/Leaflet',
       'shadowsocks/ShadowsocksX-NG', 'Homebrew/legacy-homebrew',
       'jashkenas/backbone', 'ariya/phantomjs', 'lukehoban/es6features',
       'Avik-Jain/100-Days-Of-ML-Code',
       'exacity/deeplearningbook-chinese', 'zenorocha/clipboard.js',
       'foundation/foundation-sites', 'huginn/huginn', 'videojs/video.js',
       'testerSunshine/12306', 'JuliaLang/julia', 'nuxt/nuxt.js',
       'isocpp/CppCoreGuidelines', 'RocketChat/Rocket.Chat',
       'certbot/certbot', 'codepath/android_guides', 'quilljs/quill',
       'tastejs/todomvc', 'bilibili/ijkplayer', 'caolan/async',
       'bayandin/awesome-awesomeness', 'vuetifyjs/vuetify',
       'fffaraz/awesome-cpp', 'mathiasbynens/dotfiles', 'symfony/symfony',
       'facebookresearch/Detectron', 'google-research/bert',
       'pi-hole/pi-hole', 'freeCodeCamp/devdocs', 'fxsjy/jieba',
       'istio/istio', 'raywenderlich/swift-algorithm-club',
       'alacritty/alacritty', 'JakeWharton/butterknife',
       'ant-design/ant-design-pro',
       'shengxinjing/programmer-job-blacklist', 'apachecn/AiLearning',
       'pandas-dev/pandas', 'danielmiessler/SecLists',
       'aosabook/500lines', 'getsentry/sentry', 'faif/python-patterns',
       'akullpp/awesome-java', 'square/leakcanary',
       'crossoverJie/JCSprout', 'localstack/localstack', 'wg/wrk',
       'request/request', 'Tencent/weui', 'dylanaraps/pure-bash-bible',
       'nylas/nylas-mail', 'google/styleguide', 'select2/select2',
       'Modernizr/Modernizr', 'carbon-app/carbon', 'FiloSottile/mkcert',
       'madewithml/basics', 'yangshun/front-end-interview-handbook',
       'ngosang/trackerslist', 'johnpapa/angular-styleguide',
       'Alvin9999/new-pac', 'houshanren/hangzhou_house_knowledge',
       'astaxie/beego', 'fzaninotto/Faker', 'nvie/gitflow', 'iina/iina',
       'vuejs/vuex', 'nolimits4web/swiper', 'standard/standard',
       'ZuzooVn/machine-learning-for-software-engineers',
       'jakevdp/PythonDataScienceHandbook', 'Marak/faker.js',
       'pingcap/tidb', 'netty/netty', 'ziadoz/awesome-php',
       'rethinkdb/rethinkdb', 'github/fetch', 'tailwindcss/tailwindcss',
       'dkhamsing/open-source-ios-apps',
       'herrbischoff/awesome-macos-command-line', 'jiahaog/nativefier',
       'angular/angular-cli', 'alibaba/fastjson', 'florinpop17/app-ideas',
       'ajaxorg/ace', 'naptha/tesseract.js', 'emberjs/ember.js',
       'kelseyhightower/kubernetes-the-hard-way', 'agalwood/Motrix',
       'Polymer/polymer', 'alibaba/arthas', 'hammerjs/hammer.js',
       'Automattic/mongoose', 'openai/gym', 'fighting41love/funNLP',
       'pure-css/pure', 'heartcombo/devise', 'google/leveldb',
       'fouber/blog', 'satwikkansal/wtfpython', 't4t5/sweetalert',
       'facebook/flow', 'Homebrew/brew', 'unknwon/the-way-to-go_ZH_CN',
       'gitlabhq/gitlabhq', 'hashicorp/terraform', 'harvesthq/chosen',
       'minio/minio', 'ReactiveX/rxjs', 'cheeriojs/cheerio',
       'sequelize/sequelize', 'dcloudio/uni-app', 'webtorrent/webtorrent',
       'mobxjs/mobx', 'remy/nodemon', 'niklasvh/html2canvas',
       'rapid7/metasploit-framework', 'akveo/ngx-admin',
       'cypress-io/cypress', 'redux-saga/redux-saga', 'pypa/pipenv',
       'littlecodersh/ItChat', 'balderdashy/sails',
       'scwang90/SmartRefreshLayout',
       'terryum/awesome-deep-learning-papers', 'tootsuite/mastodon',
       'alibaba/flutter-go', 'drone/drone', 'StreisandEffect/streisand',
       'eugenp/tutorials', 'ocornut/imgui',
       'NationalSecurityAgency/ghidra', 'rstacruz/nprogress',
       'ctripcorp/apollo', 'wagoodman/dive', 'microsoft/monaco-editor',
       'SortableJS/Sortable', 'koalaman/shellcheck',
       'FezVrasta/bootstrap-material-design', 'JedWatson/react-select',
       'aria2/aria2', 'kriasoft/react-starter-kit', 'syl20bnr/spacemacs',
       'CymChad/BaseRecyclerViewAdapterHelper', 'gorhill/uBlock',
       'SwiftGGTeam/the-swift-programming-language-in-chinese',
       'powerline/fonts', 'byoungd/English-level-up-tips-for-Chinese',
       'mochajs/mocha', 'guzzle/guzzle', 'typeorm/typeorm',
       'markerikson/react-redux-links', 'BradLarson/GPUImage',
       'hashicorp/consul', 'usablica/intro.js', 'dhg/Skeleton',
       'ruanyf/jstraining', 'parse-community/parse-server',
       'Seldaek/monolog', 'jaredhanson/passport', 'd2l-ai/d2l-zh',
       'CMU-Perceptual-Computing-Lab/openpose', 'vuejs/vue-devtools',
       'keon/algorithms', 'jorgebucaran/hyperapp', 'docker/compose',
       'github/hub', 'obsproject/obs-studio', 'airbnb/lottie-ios',
       'SwiftyJSON/SwiftyJSON', 'railsware/upterm',
       'PowerShell/PowerShell', 'pyenv/pyenv', 'hankcs/HanLP',
       'reduxjs/react-redux', 'pcottle/learnGitBranching',
       'bcit-ci/CodeIgniter', 'fastai/fastai', 'mongodb/mongo',
       'tj/commander.js', 'avajs/ava', 'google/gson',
       'veggiemonk/awesome-docker', 'xi-editor/xi-editor',
       'balena-io/etcher', 'mqyqingfeng/Blog', 'doczjs/docz',
       'nlohmann/json', 'inconshreveable/ngrok', 'jinzhu/gorm',
       'NativeScript/NativeScript', 'google/web-starter-kit',
       'donnemartin/data-science-ipython-notebooks', 'ReactiveX/RxSwift',
       'postcss/autoprefixer'
]

# REPOS = [
#     "gocodeup/codeup-setup-script",
#     "gocodeup/movies-application",
#     "torvalds/linux",
# ]

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        return repo_info.get("language", None)
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    readme_download_url = get_readme_download_url(contents)
    if readme_download_url == "":
        readme_contents = None
    else:
        readme_contents = requests.get(readme_download_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]


if __name__ == "__main__":
    data = scrape_github_data()
    json.dump(data, open("data.json", "w"), indent=1)