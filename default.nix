with import <nixpkgs> {};
let
    name = "message_server-env";
    pythonEnv = python38.withPackages (ps: [
        ps.colorama
        ps.pytest_6
        ps.unittest2
        ps.autopep8
        ps.flake8
        ps.flask
        ps.psycopg2
        ps.sqlalchemy
  ]);
in mkShell {
    buildInputs = [
        pythonEnv

        black
        mypy
  ];
}