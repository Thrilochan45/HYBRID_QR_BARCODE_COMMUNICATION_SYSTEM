import sys
if len(sys.argv) < 2:
    print("Usage: python run.py [gui|api]")
    sys.exit(1)

mode = sys.argv[1].lower()
if mode == "gui":
    from gui.app import main
    main()
elif mode == "api":
    from api.server import create_app
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    print("Unknown mode. choose 'gui' or 'api'")
