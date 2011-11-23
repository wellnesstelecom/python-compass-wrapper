# Compass Wrapper

Very strict in args

# Usage ...

    from compass import Compass

    compass = Compass({
        'sass_dir': '/path/must/exists',
        'css_dir': '/path/must/exists',
        'boring': True,
        'relative_assets': True,
        'output_style': 'compressed'
    })
    compass.compile()  # run 'compass compile --boring --relative-assets --output-style :compressed --sass-dir /path/must/exists --css-dir /path/must/exists'
