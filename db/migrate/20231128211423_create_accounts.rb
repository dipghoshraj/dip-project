class CreateAccounts < ActiveRecord::Migration[7.1]
  def change
    create_table :accounts, id: false do |t|
      t.primary_key :id
      t.string :auth_id
      t.string :user_name
    end
  end
end
