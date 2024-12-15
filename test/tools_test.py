
from aichatlite.core.tools import GitHubSearch,YouTubeSearch


def main():
    github_search = YouTubeSearch(name='github')
    # github_search.fetch("andrew karpathy Let's build GPT: from scratch, in code, spelled out. ")
    # print(github_search.fetch_result)
    new_query = github_search.new_query([
        "andrew karpathy Let's build GPT: from scratch, in code, spelled out. ",
        "Andrew Karpathy GPT from scratch code walkthrough",
        "Andrew Karpathy GPT from scratch code tutorial",
        "Andrew Karpathy GPT from scratch code explanation"
    ])
    print(new_query)
    # print(github_search.compress_result)


if __name__ == '__main__':
    main()