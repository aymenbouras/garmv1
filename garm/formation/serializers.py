from rest_framework import serializers
from models import Course, Chapter, SubChapter, Media, Skill


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'name', 'slug', 'media_type', 'file', 'description', 'uploaded_at']


class SubChapterSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, required=False)  # Nested media

    class Meta:
        model = SubChapter
        fields = ['id', 'name', 'slug', 'content', 'order', 'media', 'estimated_time', 'version']

    def create(self, validated_data):
        media_data = validated_data.pop('media', [])
        subchapter = SubChapter.objects.create(**validated_data)

        for media in media_data:
            Media.objects.create(subchapter=subchapter, **media)

        return subchapter


class ChapterSerializer(serializers.ModelSerializer):
    subchapters = SubChapterSerializer(many=True, required=False)  # Nested subchapters

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'slug', 'content', 'order', 'subchapters', 'estimated_time', 'version']

    def create(self, validated_data):
        subchapters_data = validated_data.pop('subchapters', [])
        chapter = Chapter.objects.create(**validated_data)

        for subchapter in subchapters_data:
            subchapter['chapter'] = chapter
            SubChapterSerializer.create(SubChapterSerializer(), validated_data=subchapter)

        return chapter


class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, required=False)  # Nested chapters
    skills = serializers.SlugRelatedField(many=True, slug_field='name',
                                          queryset=Skill.objects.all())  # Skills using slugs

    class Meta:
        model = Course
        fields = ['id', 'name', 'slug', 'description', 'duration', 'cover_image', 'skills', 'chapters',
                  'certification_exam']

    def create(self, validated_data):
        chapters_data = validated_data.pop('chapters', [])
        skills_data = validated_data.pop('skills', [])
        course = Course.objects.create(**validated_data)

        course.skills.set(skills_data)

        for chapter_data in chapters_data:
            chapter_data['course'] = course
            ChapterSerializer.create(ChapterSerializer(), validated_data=chapter_data)

        return course
