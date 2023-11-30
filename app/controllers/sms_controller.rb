class SmsController < ApplicationController
    
    skip_before_action :verify_authenticity_token
    before_action :authenticate_caller, :validate_parameters

    before_action :check_rate_limit, only: [:outbound]


    def inbound
        to, from, text = sms_params[:to], sms_params[:from], sms_params[:text]

        phone_number = PhoneNumber.find_by(number: to, account_id: @current_account.id)
        return render json: { message: "", error: "to parameter not found"}, status: 400 unless phone_number.present?

        $redis.set("calls:#{to.to_s}_#{from.to_s}", to.to_s, ex: 14400) if  text.downcase.include?("stop")
        render json: { message: "inbound sms ok" }, status: 200
    end


    def outbound
        to, from, text = sms_params[:to], sms_params[:from], sms_params[:text]



        key = "calls:#{from.to_s}_#{to.to_s}"
        data = $redis.get(key)
        puts key, data
        return render json: {message: "", error: "sms from #{from} to #{to} blocked by STOP request"}, status: 400 unless data.nil?

        phone_number = PhoneNumber.find_by(number: from, account_id: @current_account.id)
        return render json: {message: "", error: "from parameter not found"}, status: 400 if phone_number.nil?
        render json: { message: 'outbound sms ok' }, status: 200
    end


    private


    def validate_parameters
        to, from, text = sms_params[:to], sms_params[:from], sms_params[:text]       
        sms_params.each do |key, value|
            return render json: { message:"", error: "#{key} missing parameter" }, status: 400 if value.blank?
        end
        return render json: {message: "", error:"to is invalid"}, status: 400 unless to.is_a?(String) && positive_numeric?(to) && to.length >= 6 && to.length <= 16
        return render json: {message: "", error:"from is invalid"}, status: 400 unless from.is_a?(String) && positive_numeric?(from) && from.length >= 6 && from.length <= 16
        return render json: {message: "", error:"text is invalid"}, status: 400 unless text.is_a?(String) && text.length < 120
    end

    def positive_numeric?(str)
        !!(str.to_s =~ /\A[1-9]\d*\z/)
    end


    def check_rate_limit
        key = "user_calling_outbound:#{sms_params[:from]}"
        count = $redis.get(key).to_i
        puts "count: #{count}"
        return render json: { message:"", error: "limit reached for from #{sms_params[:from]}"}, status: 400 if count >= 50

        $redis.incr(key)
        $redis.expire(key, 24.hours.to_i)
    end
      

    def sms_params
        params.permit(:from, :to, :text)
    end
end
