def init(application):
    @application.route('/')
    def he():
        return "<h1 style='text-align: center'>BIBA PASASIBA</h1>"

