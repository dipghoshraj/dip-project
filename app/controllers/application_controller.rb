class ApplicationController < ActionController::Base

    protect_from_forgery with: :null_session

    def authenticate_caller
        authenticate_or_request_with_http_basic do |username, password|

            render_api_error(403, "Invalid authentication") if not username or not password
            @current_account = Account.find_by(auth_id: password, username: username)
            render_api_error(403, "Invalid authentication") unless @current_account.present?
            @current_account
        end
    end


    def render_api_error(status_code, message = nil )
        error = {}
        error["message"] = ""
        error["error"] = message
        render json: error, status: status_code
    end

end
