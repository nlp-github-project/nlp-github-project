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


REPOS = ['vuejs/vue', 'EbookFoundation/free-programming-books',
    'tensorflow/tensorflow', 'twbs/bootstrap', 'sindresorhus/awesome',
    'getify/You-Dont-Know-JS', 'jwasham/coding-interview-university',
    'ohmyzsh/ohmyzsh', 'kamranahmedse/developer-roadmap',
    'github/gitignore', 'CyC2018/CS-Notes',
    'donnemartin/system-design-primer', 'microsoft/vscode',
    'airbnb/javascript', 'flutter/flutter', 'd3/d3', 'torvalds/linux',
    'facebook/react-native', 'jackfrued/Python-100-Days',
    'public-apis/public-apis', 'vinta/awesome-python',
    'Snailclimb/JavaGuide', 'facebook/create-react-app',
    'jlevy/the-art-of-command-line', 'TheAlgorithms/Python',
    'danistefanovic/build-your-own-x', 'axios/axios', 'golang/go',
    'trekhleb/javascript-algorithms', 'nodejs/node',
    'justjavac/free-programming-books-zh_CN', 'ytdl-org/youtube-dl',
    'animate-css/animate.css', 'kubernetes/kubernetes',
    'tensorflow/models', 'FortAwesome/Font-Awesome',
    'puppeteer/puppeteer', 'denoland/deno', 'angular/angular',
    'mrdoob/three.js', 'microsoft/TypeScript', 'ossu/computer-science',
    'ant-design/ant-design', 'angular/angular.js', 'laravel/laravel',
    'iluwatar/java-design-patterns', 'mui-org/material-ui',
    'moby/moby', '30-seconds/30-seconds-of-code',
    'PanJiaChen/vue-element-admin', 'MisterBooo/LeetCodeAnimation',
    'avelino/awesome-go', 'vuejs/awesome-vue', 'webpack/webpack',
    'nvbn/thefuck', 'jquery/jquery', 'reduxjs/redux', 'atom/atom',
    'hakimel/reveal.js', 'apple/swift', 'pallets/flask',
    'socketio/socket.io', 'django/django',
    'shadowsocks/shadowsocks-windows', 'elastic/elasticsearch',
    'vercel/next.js', 'chartjs/Chart.js', 'storybookjs/storybook',
    'expressjs/express', 'keras-team/keras',
    'spring-projects/spring-boot', 'Semantic-Org/Semantic-UI',
    'tonsky/FiraCode', 'typicode/json-server', 'chrislgarry/Apollo-11',
    'netdata/netdata', 'jakubroztocil/httpie', 'adam-p/markdown-here',
    'rails/rails', 'xingshaocheng/architect-awesome',
    'ElemeFE/element', 'goldbergyoni/nodebestpractices',
    'h5bp/html5-boilerplate', 'rust-lang/rust', 'opencv/opencv',
    'juliangarnier/anime', 'ripienaar/free-for-dev', 'grafana/grafana',
    'nodejs/node-v0.x-archive', 'x64dbg/x64dbg',
    'ziishaned/learn-regex',
    'astaxie/build-web-application-with-golang', 'ColorlibHQ/AdminLTE',
    'tesseract-ocr/tesseract', 'gogs/gogs', 'macrozheng/mall',
    'vsouza/awesome-ios', 'ageitgey/face_recognition',
    'parcel-bundler/parcel', 'square/retrofit', 'impress/impress.js',
    'MaximAbramchuck/awesome-interview-questions', 'sveltejs/svelte',
    'TryGhost/Ghost', 'k88hudson/git-flight-rules',
    'Alamofire/Alamofire', 'home-assistant/core',
    'prakhar1989/awesome-courses', 'vercel/hyper',
    'bailicangdu/vue2-elm', 'soimort/you-get',
    'tuvtran/project-based-learning', 'azl397985856/leetcode',
    'AFNetworking/AFNetworking', 'git/git', 'shadowsocks/shadowsocks',
    'trimstray/the-book-of-secret-knowledge', 'Unitech/pm2',
    'apache/dubbo', 'v2ray/v2ray-core', 'leonardomso/33-js-concepts',
    'JetBrains/kotlin',
    'sdmg15/Best-websites-a-programmer-should-visit', 'gulpjs/gulp',
    'cdr/code-server', 'google/material-design-lite',
    'justjavac/awesome-wechat-weapp', 'python/cpython',
    'syncthing/syncthing', 'adobe/brackets', 'Genymobile/scrcpy',
    'etcd-io/etcd', 'facebook/jest', 'prometheus/prometheus',
    'karan/Projects', 'mozilla/pdf.js', 'PhilJay/MPAndroidChart',
    'discourse/discourse', 'godotengine/godot',
    '521xueweihan/HelloGitHub', 'blueimp/jQuery-File-Upload',
    'deepfakes/faceswap', 'hexojs/hexo', 'BVLC/caffe',
    'mermaid-js/mermaid', 'Solido/awesome-flutter',
    'huggingface/transformers', 'Leaflet/Leaflet',
    'Homebrew/legacy-homebrew', 'jashkenas/backbone',
    'lukehoban/es6features', 'nuxt/nuxt.js',
    'isocpp/CppCoreGuidelines', 'nestjs/nest', 'iamkun/dayjs',
    'netty/netty', 'ziadoz/awesome-php', 'rethinkdb/rethinkdb',
    'herrbischoff/awesome-macos-command-line', 'jiahaog/nativefier',
    'angular/angular-cli', 'mathiasbynens/dotfiles', 'symfony/symfony',
    'facebookresearch/Detectron', 'iview/iview',
    'faif/python-patterns', 'akullpp/awesome-java',
    'square/leakcanary', 'crossoverJie/JCSprout',
    'localstack/localstack', 'request/request', 'Tencent/weui',
    'dylanaraps/pure-bash-bible', 'nylas/nylas-mail',
    'google/styleguide', 'NationalSecurityAgency/ghidra',
    'rstacruz/nprogress', 'ctripcorp/apollo', 'cmderdev/cmder',
    'airbnb/lottie-web', 'metabase/metabase', 'openai/gym',
    'fighting41love/funNLP', 'pure-css/pure', 'heartcombo/devise',
    'scwang90/SmartRefreshLayout', 'fouber/blog', 't4t5/sweetalert',
    'remy/nodemon', 'facebook/flow', 'gorhill/uBlock',
    'niklasvh/html2canvas', 'akveo/ngx-admin', 'cypress-io/cypress',
    'redux-saga/redux-saga', 'SortableJS/Sortable',
    'koalaman/shellcheck', 'aria2/aria2', 'sharkdp/bat',
    'kriasoft/react-starter-kit', 'syl20bnr/spacemacs',
    'BurntSushi/ripgrep', 'GoogleChrome/lighthouse',
    'mbeaudru/modern-js-cheatsheet',
    'kon9chunkit/GitHub-Chinese-Top-Charts', 'fzaninotto/Faker',
    'nvie/gitflow', 'iina/iina', 'vuejs/vuex', 'nolimits4web/swiper',
    'standard/standard',
    'ZuzooVn/machine-learning-for-software-engineers',
    'jakevdp/PythonDataScienceHandbook', 'Marak/faker.js',
    'pingcap/tidb', 'github/fetch', 'tailwindcss/tailwindcss',
    'dkhamsing/open-source-ios-apps',
    'brillout/awesome-react-components', 'transloadit/uppy',
    '3b1b/manim', 'greenrobot/EventBus', 'CSSEGISandData/COVID-19',
    'markedjs/marked', 'GitbookIO/gitbook', 'date-fns/date-fns',
    'lib-pku/libpku', 'skylot/jadx', 'dotnet/corefx',
    'bilibili/flv.js', 'nsqio/nsq', 'SeleniumHQ/selenium',
    'JohnCoates/Aerial', 'swagger-api/swagger-ui',
    'QSCTech/zju-icicles', 'SnapKit/Masonry', 'pjreddie/darknet',
    'afollestad/material-dialogs', 'freeCodeCamp/freeCodeCamp',
    '996icu/996.ICU', 'facebook/react', 'electron/electron',
    'microsoft/terminal', 'lodash/lodash',
    'josephmisiti/awesome-machine-learning', 'kdn251/interviews',
    'h5bp/Front-end-Developer-Interview-Questions',
    'resume/resume.github.com']

# REPOS = [
#     "gocodeup/codeup-setup-script",
#     "gocodeup/movies-application",
#     "torvalds/linux",
#     "harthur/brain",
#     "google/agera",
#     "michaeltyson/TPKeyboardAvoiding",
#     "bendc/sprint",
#     "rengwuxian/RxJavaSamples",
#     "fastos/fastsocket",
#     "petruisfan/node-supervisor"
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
    readme_contents = requests.get(get_readme_download_url(contents)).text
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
