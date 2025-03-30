# comp7940_Project

As mainland can not connect to docker hub, I used anzure images resp to manage online images

# anzure container update processes: (7940project is images name and comp7940project is anzure appname)
1. docker build -t 7940project .
2. docker tag 7940project 24428078images.azurecr.io/7940project
3. az login
4. az acr login -n 24428078images 
5. docker push 24428078images.azurecr.io/7940project
6. az containerapp update --name comp7940project --resource-group 24428078 --image 24428078images.azurecr.io/7940project:latest (auto)

# db structure example:
{
	"_id" : ObjectId("67e9254014e28a7020255a2a"),
	"question_content" : {
		"text" : "What is the capital of France?",
		"options" : [
			{
				"option" : "A",
				"text" : "Paris"
			},
			{
				"option" : "B",
				"text" : "London"
			},
			{
				"option" : "C",
				"text" : "Berlin"
			},
			{
				"option" : "D",
				"text" : "Madrid"
			}
		]
	},
	"question_type" : 1,
	"answer" : "A",
	"type" : [
		"geography",
		"capital cities"
	]
},
{
	"_id" : ObjectId("67e9300e04d760fa5fde84d0"),
	"question_content" : "The Earth is the third planet from the Sun.",
	"question_type" : 2,
	"answer" : "True",
	"type" : [
		"astronomy",
		"solar system"
	]
},
{
	"_id" : ObjectId("67e9300e04d760fa5fde84d1"),
	"question_content" : "Describe the process of photosynthesis.",
	"question_type" : 3,
	"answer" : "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll.",
	"type" : [
		"biology",
		"plant science"
	]
}
{
	"_id" : ObjectId("67e9753e7430db5ef8d6f1d5"),
	"question_content" : {
		"text" : "What is db",
		"options" : [ ]
	},
	"question_type" : 3,
	"answer" : "Db is noting",
	"type" : [
		"Database"
	]
}

# bot 
t.me/comp_7940_exam_bot.
/hello A test command
/anzureConnect A test command
/findQuestion Find number of questions from db
/answer Get answer from found questions
/askGpt Ask gpt a found question
/deleteQuestion Delete a found question