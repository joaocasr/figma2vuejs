import os

def overwrite_styling(name):
    print("Updating global css properties...")
    maincss="""@import './base.css';


@media (min-width: 1024px) {
  #app {
      padding: 0;
  }
}
"""
    filemain = "../output/"+name+"/src/assets/main.css"
    if os.path.isfile(filemain):
        f= open(filemain,"w")
        f.write(maincss)
        f.close()
        basecss= """/* color palette from <https://github.com/vuejs/theme> */
:root {
  --vt-c-white: #ffffff;
  --vt-c-white-soft: #f8f8f8;
  --vt-c-white-mute: #f2f2f2;

  --vt-c-black: #181818;
  --vt-c-black-soft: #222222;
  --vt-c-black-mute: #282828;

  --vt-c-indigo: #2c3e50;

  --vt-c-divider-light-1: rgba(60, 60, 60, 0.29);
  --vt-c-divider-light-2: rgba(60, 60, 60, 0.12);
  --vt-c-divider-dark-1: rgba(84, 84, 84, 0.65);
  --vt-c-divider-dark-2: rgba(84, 84, 84, 0.48);

  --vt-c-text-light-1: var(--vt-c-indigo);
  --vt-c-text-light-2: rgba(60, 60, 60, 0.66);
  --vt-c-text-dark-1: var(--vt-c-white);
  --vt-c-text-dark-2: rgba(235, 235, 235, 0.64);
}

/* semantic color variables for this project */
:root {
  --color-background: var(--vt-c-white);
  --color-background-soft: var(--vt-c-white-soft);
  --color-background-mute: var(--vt-c-white-mute);

  --color-border: var(--vt-c-divider-light-2);
  --color-border-hover: var(--vt-c-divider-light-1);

  --color-heading: var(--vt-c-text-light-1);
  --color-text: var(--vt-c-text-light-1);

  --section-gap: 160px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-background: var(--vt-c-black);
    --color-background-soft: var(--vt-c-black-soft);
    --color-background-mute: var(--vt-c-black-mute);

    --color-border: var(--vt-c-divider-dark-2);
    --color-border-hover: var(--vt-c-divider-dark-1);

    --color-heading: var(--vt-c-text-dark-1);
    --color-text: var(--vt-c-text-dark-2);
  }
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  font-weight: normal;
}

body {
  margin:0px;
}
"""
    else:
        raise Exception("main.css file not found!")
    filebase = "../output/"+name+"/src/assets/base.css"
    if os.path.isfile(filebase):
        f= open(filebase,"w")
        f.write(basecss)
        f.close()
    else:
        raise Exception("base.css file not found!")


def generatePageStyle(name,page):
  width = page.containerstyle.width
  height = page.containerstyle.height
  css = """.grid-container {
    display:"""+ page.containerstyle.display+ """;
    grid-template-columns:"""+ page.containerstyle.gridtemplatecolumns+""";
    grid-template-rows:"""+ page.containerstyle.gridtemplaterows + """;
    background-color:"""+ page.containerstyle.backgroundColor + """;
    width: 100%;
    min-height: 100vh;
    max-height: auto;
    margin:"""+ page.containerstyle.margin + """;
    padding:"""+ page.containerstyle.padding + """;
  }
  
  .grid-item {
    display:flex;
    text-align: center;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    grid-column: calc(var(--posx) * 16 / """+ str(width)+"""); 
    grid-row: calc(var(--posy) * 16 / """+ str(height)+ """);
}
  """
  with open("../output/"+name+"/src/assets/"+page.getPagename().lower()+".css","w") as f:
    f.write(css)

